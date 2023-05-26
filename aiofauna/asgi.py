import asyncio
import io
import typing
from typing import Awaitable, Callable, Dict, Literal, MutableMapping, Tuple

from aiohttp import web
from aiohttp.http_parser import RawRequestMessage
from aiohttp.payload import StringPayload
from multidict import CIMultiDict, CIMultiDictProxy, MultiDict
from yarl import URL

from aiofauna import Api

Scope = MutableMapping[str, typing.Any]
Message = MutableMapping[str, typing.Any]
Receive = Callable[[], Awaitable[Message]]
Send = Callable[[Message], Awaitable[None]]

ASGIApp = Callable[[Scope, Receive, Send], Awaitable[None]]


class ASGIApi(Api):
    """
    An ASGI-compatible API.

    Currently only supports HTTP and is compatible with ASGI 2.0.

    Tested with:
    `uvicorn`
    `daphne`[TODO]

    """

    async def asgi(self, scope: Scope, _, send: Send) -> None:
        """ASGI Wrapper."""

        if scope["type"] != "http":
            raise RuntimeError("Only HTTP is supported")

        raw_headers: Tuple[Tuple[bytes, bytes], ...] = scope["headers"]
        headers: Dict[str, str] = {}
        for k, v in raw_headers:
            headers[k.decode().lower()] = v.decode()

        message = RawRequestMessage(
            method=scope["method"],
            path=scope["path"],
            version=scope["http_version"],
            headers=CIMultiDictProxy(CIMultiDict(MultiDict(headers))),
            raw_headers=raw_headers,
            should_close=True,
            compression=None,
            upgrade=False,
            chunked=True,
            url=URL(scope["path"]),
        )

        class _tranport:
            scheme = scope["scheme"]

            def get_extra_info(
                self, info: Literal["sslcontext"]
            ):  # pylint: disable=unused-argument
                """Mock method to match `aiohttp.web.BaseRequestTransport` contract."""
                return None

        class _proto(web.RequestHandler):
            http_version = scope["http_version"]
            transport = _tranport()

        request = web.Request(
            message=message,
            payload=io.BytesIO(),
            protocol=_proto,
            payload_writer=None,
            task=None,
            loop=asyncio.get_running_loop(),
        )

        response = await self._handle(request)

        body = response._body
        if isinstance(body, StringPayload):
            body = body._value
        if isinstance(body, str):
            body = body.encode()

        await send(
            {
                "type": "http.response.start",
                "status": response.status,
                "headers": [
                    (k.encode(), v.encode()) for k, v in response.headers.items()
                ],
            }
        )

        await send({"type": "http.response.body", "body": body, "more_body": False})

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """ASGI callable."""
        return await self.asgi(scope, receive, send)
