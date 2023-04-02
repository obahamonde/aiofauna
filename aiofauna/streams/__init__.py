from typing import Optional
import asyncio
import contextlib
import io
import re

from aiohttp.web import HTTPMethodNotAllowed, StreamResponse

from aiofauna.streams.eventctx import _ContextManager

__version__ = "2.1.0"
__all__ = ["EventSourceResponse", "sse_response"]


class EventSourceResponse(StreamResponse):
    """
    A class for creating Server-Sent Events (SSE) responses using aiohttp's StreamResponse.

    Attributes:
    DEFAULT_PING_INTERVAL (int): The default interval (in seconds) at which to send ping messages to keep the connection alive.
    DEFAULT_SEPARATOR (str): The default separator to use between event messages.
    LINE_SEP_EXPR (re.Pattern): The regular expression used to match line separators in messages.

    Args:
    status (int): HTTP status code (default: 200).
    reason (str): HTTP reason phrase.
    headers (dict): A dictionary containing HTTP headers (default: None).
    sep (str): The separator to use between event messages (default: DEFAULT_SEPARATOR).
    """
    DEFAULT_PING_INTERVAL = 15
    DEFAULT_SEPARATOR = "\r\n"
    LINE_SEP_EXPR = re.compile(r"\r\n|\r|\n")

    def __init__(self, *, status=200, reason=None, headers=None, sep=None):
        super().__init__(status=status, reason=reason)

        if headers is not None:
            self.headers.extend(headers)

        # mandatory for servers-sent events headers
        self.headers["Content-Type"] = "text/event-stream"
        self.headers["Cache-Control"] = "no-cache"
        self.headers["Connection"] = "keep-alive"
        self.headers["X-Accel-Buffering"] = "no"

        self._ping_interval = self.DEFAULT_PING_INTERVAL
        self._ping_task = None
        self._sep = sep if sep is not None else self.DEFAULT_SEPARATOR

    async def _prepare(self, request):
        """
        Prepares for streaming and sends HTTP headers.

        Args:
        request (aiohttp.web.Request): The request object.

        Returns:
        The prepared response object.
        """
        await self.prepare(request)
        return self

    async def prepare(self, request):
        """
        Prepares for streaming and sends HTTP headers.

        Args:
        request (aiohttp.web.Request): The request object.

        Raises:
        HTTPMethodNotAllowed: If the request method is not GET or HEAD.
        asyncio.CancelledError: If the request is disconnected.
        """
        if request.method not in {"GET", "HEAD"}:
            raise HTTPMethodNotAllowed(request.method, ["GET", "HEAD"])

        if not self.prepared:
            writer = await super().prepare(request)
            self._ping_task = asyncio.create_task(self._ping())
            # explicitly enabling chunked encoding, since content length
            # usually not known beforehand.
            self.enable_chunked_encoding()
            return writer
            #`[WIP]`
            # https://github.com/aio-libs/aiohttp/issues/3105
        if request.protocol.transport is None:
            # request disconnected
            raise asyncio.CancelledError()
        else:
            await super().prepare(request)


    async def send(self, data, id: Optional[str] = None, event: Optional[str] = None, retry: Optional[int] = None):
        """
        Sends a Server-Sent Event to the client.

        Args:
        data (str): The message to send.
        id (str): An optional identifier for the event.
        event (str): An optional event name.
        retry (int): An optional retry time (in milliseconds) for the client to wait before attempting to reconnect.

        Raises:
        TypeError: If retry is not an integer.
        """
        buffer = io.StringIO()
        if id is not None:
            buffer.write(self.LINE_SEP_EXPR.sub("", f"id: {id}"))
            buffer.write(self._sep)

        if event is not None:
            buffer.write(self.LINE_SEP_EXPR.sub("", f"event: {event}"))
            buffer.write(self._sep)

        for chunk in self.LINE_SEP_EXPR.split(data):
            buffer.write(f"data: {chunk}")
            buffer.write(self._sep)

        if retry is not None:
            if not isinstance(retry, int):
                raise TypeError("retry argument must be int")
            buffer.write(f"retry: {retry}")
            buffer.write(self._sep)

        buffer.write(self._sep)
        await self.write(buffer.getvalue().encode("utf-8"))

    async def wait(self):
        """
        Waits for the response to complete.

        Raises:
        RuntimeError: If the response has not been started.
        """
        if self._ping_task is None:
            raise RuntimeError("Response is not started")
        with contextlib.suppress(asyncio.CancelledError):
            await self._ping_task

    def stop_streaming(self):
        """
        Stops streaming the response.

        Raises:
        RuntimeError: If the response has not been started.
        """
        if self._ping_task is None:
            raise RuntimeError("Response is not started")
        self._ping_task.cancel()

    def enable_compression(self, request):
        """
        Enables compression for the response.

        Args:
        request (aiohttp.web.Request): The request object.

        Raises:
        RuntimeError: If the response has already been started.
        """
        if self._ping_task is not None:
            raise RuntimeError("Response is already started")
        super().enable_compression(request)
        
        
    @property
    def ping_interval(self):
        """
        Gets the interval (in seconds) at which to send ping messages to keep the connection alive.

        Returns:
        The ping interval.
        """
        return self._ping_interval

    @ping_interval.setter
    def ping_interval(self, value):
        """
        Sets the interval (in seconds) at which to send ping messages to keep the connection alive.

        Args:
        value (int): The ping interval.

        Raises:
        TypeError: If value is not an integer.
        ValueError: If value is less than 0.
        """
        if not isinstance(value, int):
            raise TypeError("ping interval must be int")
        if value < 0:
            raise ValueError("ping interval cannot be < 0, Time travel is not supported")

        self._ping_interval = value

    async def _ping(self):
        """
        Sends a ping message to the client at regular intervals to keep the connection alive.
        """
        while True:
            await asyncio.sleep(self._ping_interval)
            await self.write(": ping{0}{0}".format(self._sep).encode("utf-8"))

    async def __aenter__(self):
        """
        Called when entering a context (async with).

        Returns:
        The response object.
        """
        return self

    async def __aexit__(self, *args):
        """
        Called when exiting a context (async with).

        Returns:

        None
        
        """
        self.stop_streaming()
        await self.wait()
        return None

def sse_response(
    request,
    *,
    status=200,
    reason=None,
    headers=None,
    sep=None,
    response_cls=EventSourceResponse,
):
    """
    `sse_response` is a helper function for creating a context manager
    that will handle an `EventSource` network connection from the client
    inside a context manager that will stream `utf-8` encoded data to the
    client encapsulated in the `EventSource` protocol.
    
    Usage:
    
    ```python
    
    from datetime import datetime
    
    async def handler(request):
        async with sse_response(request) as resp:
            while True:
                await resp.send(datetime.now().isoformat())
                await asyncio.sleep(1)
        return resp
    ```    
    """
    if not issubclass(response_cls, EventSourceResponse):
        raise TypeError(
            "response_cls must be subclass of "
            "aiohttp_sse.EventSourceResponse, got {}".format(response_cls)
        )

    sse = response_cls(status=status, reason=reason, headers=headers, sep=sep)
    return _ContextManager(sse._prepare(request))
