"""ASGI Middleware"""
import typing
import io
from aiofauna.application import App, Request

Scope = typing.MutableMapping[str, typing.Any]
Message = typing.MutableMapping[str, typing.Any]

Receive = typing.Callable[[], typing.Awaitable[Message]]
Send = typing.Callable[[Message], typing.Awaitable[None]]

ASGIApp = typing.Callable[[Scope, Receive, Send], typing.Awaitable[None]]


def aioasgi(app: App) -> ASGIApp:
    """
    Converts an aiohttp web application to an ASGI application.

    Args:
        app (App): An instance of the aiohttp web application.

    Returns:
        ASGIApp: An instance of the ASGI application.

    Raises:
        RuntimeError: If the ASGI scope is not of type "http".

    Notes:
        This middleware function is used to convert an aiohttp web application
        to an ASGI application, so that it can be used with ASGI-compatible web
        servers.

        The resulting ASGI application can be used with any ASGI-compatible web
        server, including Uvicorn, Daphne, and Hypercorn.

    Examples:
        Here's an example of how to use the `aiohttp_to_asgi` middleware function:

        ```python
        from aiohttp import web
        from aiofauna import App
        from myapp import routes

        app = App()
        app.add_routes(routes)

        asgi_app = aiohttp_to_asgi(app)

        from uvicorn import run
        
        run(asgi_app)
        
        ```
    """

    async def asgi(scope: Scope, receive: Receive, send: Send) -> None:
        nonlocal app
        if scope["type"] != "http":
            raise RuntimeError("Only HTTP is supported")

        method = scope["method"]
        path = scope["path"]
        query_string = scope.get("query_string", b"").decode()
        headers = [[key.decode(), value.decode()] for key, value in scope["headers"]]
        body = b""

        content_length = int(scope.get("content_length", 0))

        while content_length:
            message = await receive()
            _body = message.get("body", b"")
            body += _body
            content_length -= len(_body)

        request = Request(
            method=method,
            path=path,
            query_string=query_string,
            headers=headers,
            body=body,
        )

        response = await app._handle(request)  # pylint: disable=protected-access

        body_length = response.body_length

        response_body = b""

        while body_length:
            if response.chunked:
                writer = response._payload_writer  # pylint: disable=protected-access
                if writer is None:
                    response_body = (
                        response._content_dict
                    )  # pylint: disable=protected-access
                    break
                buffer_size = writer.buffer_size
                with io.BytesIO() as buffer:
                    while buffer_size:
                        await writer.drain()
                        chunk = response._body  # pylint: disable=protected-access
                        if not chunk:  # pylint: disable=protected-access
                            break
                        if isinstance(chunk, bytes):
                            buffer.write(chunk)
                            buffer_size -= len(chunk)
                        elif isinstance(chunk, str):
                            buffer.write(chunk.encode())
                            buffer_size -= len(chunk.encode())
                        else:
                            raise RuntimeError("Invalid chunk type")
                    response_body += buffer.getvalue()
                    body_length -= len(response_body)
            else:
                response_body = (
                    response._content_dict
                )  # pylint: disable=protected-access
                break

        await send(
            {
                "type": "http.response.start",
                "status": response.status,
                "headers": response.headers,
            }
        )

        await send(
            {"type": "http.response.body", "body": response_body,}
        )

    return asgi
