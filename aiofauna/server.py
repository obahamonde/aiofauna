"""REST API Module with automatic OpenAPI generation."""
import asyncio
import os
from functools import wraps
from inspect import signature
from typing import Awaitable, Callable

from aiohttp.typedefs import Handler
from aiohttp.web import Application, FileResponse, Request, Response, StreamResponse
from aiohttp.web_middlewares import middleware
from aiohttp.web_ws import WebSocketResponse
from aiohttp_sse import EventSourceResponse, sse_response

from .client import APIClient
from .docs import HTML_STRING, extract, load, transform
from .helpers import do_response
from .json import jsonable_encoder
from .odm import FaunaModel
from .router import APIRouter
from .typedefs import Document
from .utils import setup_logging
from typing_extensions import ParamSpec

P = ParamSpec("P")

Middleware = Callable[[Request, Handler], Awaitable[StreamResponse]]


class APIServer(Application):
    """AioFauna APIServer"""

    def __init__(
        self,
        *args,
        title: str = "AioFauna",
        servers: list[str] = None,
        description: str = "AioFauna API",
        version: str = "0.0.1",
        openapi_url: str = "/openapi.json",
        **kwargs,
    ):
        super().__init__(*args, logger=setup_logging(self.__class__.__name__), **kwargs)
        schemas = FaunaModel.Metadata.subclasses + Document.Metadata.subclasses
        self.openapi = {
            "openapi": "3.0.0",
            "info": {"title": title, "version": version},
            "paths": {},
            "tags": [],
            "servers": [{"url": url} for url in servers or []],
            "components": {
                "schemas": {schema.__name__: schema.schema() for schema in schemas}
            },
            "description": description,
        }
        self._route_open_api_params = {}
        self.openapi_url = openapi_url

        @self.get("/openapi.json")
        async def openapi():
            response = jsonable_encoder(self.openapi)
            return response

        @self.get("/docs")
        async def docs():
            return Response(
                text=HTML_STRING(self.openapi_url), content_type="text/html"
            )

        @self.on_event("startup")
        async def startup(_):
            await FaunaModel.create_all()

        @self.on_event("shutdown")
        async def shutdown(_):
            await APIClient.cleanup()
            await FaunaModel.cleanup()

    def document(
        self, path: str, method: str
    ) -> Callable[
        [Callable[P, Awaitable[StreamResponse]]], Callable[P, Awaitable[StreamResponse]]
    ]:
        """

        SWAGGER DOCUMENTATION

        """

        def decorator(
            func: Callable[P, Awaitable[StreamResponse]]
        ) -> Callable[P, Awaitable[StreamResponse]]:
            sig = signature(func)
            params = sig.parameters
            open_api_params = extract(params.copy(), path)
            self._route_open_api_params[(path, method)] = open_api_params
            transform(self.openapi, path, method, func, open_api_params)

            async def wrapper(*args: P.args, **kwargs: P.kwargs) -> StreamResponse:
                request: Request = args[0]
                args = args[1:]
                args_to_apply = await load(request, params.copy())
                definitive_args = {}
                for name, param in params.items():
                    if name in args_to_apply:
                        definitive_args[name] = args_to_apply[name]
                    elif param.default is not param.empty:
                        definitive_args[name] = param.default
                    else:
                        raise ValueError(
                            f"Missing parameter {name} for {func.__name__}"
                        )
                if asyncio.iscoroutinefunction(func):
                    response = await func(*args, **kwargs, **definitive_args)
                else:
                    response = func(*args, **kwargs, **definitive_args)
                return do_response(response)

            wrapper._handler = func
            return wrapper

        return decorator

    def get(
        self, path: str, **kwargs
    ) -> Callable[
        [Callable[P, Awaitable[StreamResponse]]], Callable[P, Awaitable[StreamResponse]]
    ]:
        """GET decorator"""

        def decorator(
            func: Callable[P, Awaitable[StreamResponse]]
        ) -> Callable[P, Awaitable[StreamResponse]]:
            self.router.add_get(path, self.document(path, "GET")(func), **kwargs)
            return func

        return decorator

    def post(
        self, path: str, **kwargs
    ) -> Callable[
        [Callable[P, Awaitable[StreamResponse]]], Callable[P, Awaitable[StreamResponse]]
    ]:
        """POST decorator"""

        def decorator(
            func: Callable[P, Awaitable[StreamResponse]]
        ) -> Callable[P, Awaitable[StreamResponse]]:
            self.router.add_post(path, self.document(path, "POST")(func), **kwargs)
            return func

        return decorator

    def put(
        self, path: str, **kwargs
    ) -> Callable[
        [Callable[P, Awaitable[StreamResponse]]], Callable[P, Awaitable[StreamResponse]]
    ]:
        """PUT decorator"""

        def decorator(
            func: Callable[P, Awaitable[StreamResponse]]
        ) -> Callable[P, Awaitable[StreamResponse]]:
            self.router.add_put(path, self.document(path, "PUT")(func), **kwargs)
            return func

        return decorator

    def delete(
        self, path: str, **kwargs
    ) -> Callable[
        [Callable[P, Awaitable[StreamResponse]]], Callable[P, Awaitable[StreamResponse]]
    ]:
        """DELETE decorator"""

        def decorator(
            func: Callable[P, Awaitable[StreamResponse]]
        ) -> Callable[P, Awaitable[StreamResponse]]:
            self.router.add_delete(path, self.document(path, "DELETE")(func), **kwargs)
            return func

        return decorator

    def patch(
        self, path: str, **kwargs
    ) -> Callable[
        [Callable[P, Awaitable[StreamResponse]]], Callable[P, Awaitable[StreamResponse]]
    ]:
        """PATCH decorator"""

        def decorator(
            func: Callable[P, Awaitable[StreamResponse]]
        ) -> Callable[P, Awaitable[StreamResponse]]:
            self.router.add_patch(path, self.document(path, "PATCH")(func), **kwargs)
            return func

        return decorator

    def head(
        self, path: str, **kwargs
    ) -> Callable[
        [Callable[P, Awaitable[StreamResponse]]], Callable[P, Awaitable[StreamResponse]]
    ]:
        """HEAD decorator"""

        def decorator(
            func: Callable[P, Awaitable[StreamResponse]]
        ) -> Callable[P, Awaitable[StreamResponse]]:
            self.router.add_head(path, self.document(path, "HEAD")(func), **kwargs)
            return func

        return decorator

    def options(self, path: str, **kwargs):
        """OPTIONS decorator"""

        def decorator(
            func: Callable[P, Awaitable[StreamResponse]]
        ) -> Callable[P, Awaitable[StreamResponse]]:
            self.router.add_options(
                path, self.document(path, "OPTIONS")(func), **kwargs
            )
            return func

        return decorator

    def on_event(
        self, event: str
    ) -> Callable[
        [Callable[[Application], Awaitable[None]]],
        Callable[[Application], Awaitable[None]],
    ]:
        """On event handler"""

        def decorator(
            func: Callable[[Application], Awaitable[None]]
        ) -> Callable[[Application], Awaitable[None]]:
            if event not in ("startup", "shutdown"):
                raise ValueError("Event must be startup or shutdown")
            elif event == "startup":
                self.on_startup.append(func)
            else:
                self.on_shutdown.append(func)
            return func

        return decorator

    def sse(
        self, path: str
    ) -> Callable[
        [Callable[P, Awaitable[EventSourceResponse]]],
        Callable[P, Awaitable[EventSourceResponse]],
    ]:
        """Server Sent Events decorator"""

        def decorator(
            func: Callable[P, Awaitable[EventSourceResponse]]
        ) -> Callable[P, Awaitable[EventSourceResponse]]:
            @wraps(func)
            async def wrapper(request: Request) -> EventSourceResponse:
                async with sse_response(request) as resp:
                    args_to_apply = await load(
                        request, signature(func).parameters.copy()
                    )
                    definitive_args = {}
                    for name, param in signature(func).parameters.items():
                        if param.annotation == EventSourceResponse:
                            definitive_args[name] = resp
                        elif name in args_to_apply:
                            definitive_args[name] = args_to_apply[name]
                            args_to_apply.pop(name)
                        elif param.default is not param.empty:
                            definitive_args[name] = param.default
                        else:
                            raise ValueError(
                                f"Missing parameter {name} for {func.__name__}"
                            )
                    await func(**definitive_args)
                    return resp

            self.router.add_get(path, wrapper)
            return wrapper

        return decorator

    def websocket(
        self, path: str
    ) -> Callable[
        [Callable[P, Awaitable[WebSocketResponse]]],
        Callable[P, Awaitable[WebSocketResponse]],
    ]:
        """Websocket decorator"""

        def decorator(
            func: Callable[P, Awaitable[WebSocketResponse]]
        ) -> Callable[P, Awaitable[WebSocketResponse]]:
            @wraps(func)
            async def wrapper(request: Request):
                args_to_apply = await load(request, signature(func).parameters.copy())
                ws = WebSocketResponse()
                await ws.prepare(request)
                definitive_args = {}
                for name, param in signature(func).parameters.items():
                    if param.annotation == WebSocketResponse:
                        definitive_args[name] = ws
                    elif name in args_to_apply:
                        definitive_args[name] = args_to_apply[name]
                        args_to_apply.pop(name)
                    elif param.default is not param.empty:
                        definitive_args[name] = param.default
                    else:
                        raise ValueError(
                            f"Missing parameter {name} for {func.__name__}"
                        )
                await func(**definitive_args)
                return ws

            self.router.add_get(path, wrapper)
            return wrapper

        return decorator

    def static(self) -> "APIServer":
        """Static folder creation and serving"""

        @self.get("/")
        def index():
            return FileResponse("static/index.html")

        try:
            os.makedirs("static", exist_ok=True)
        except OSError:
            pass
        self.router.add_static("/", "static")

        return self

    def middleware(self, func: Middleware) -> Middleware:
        @wraps(func)
        @middleware
        async def wrapper(request: Request, handler: Handler) -> Response:
            response = await func(request, handler)
            if isinstance(response, Response):
                return response
            return do_response(response)

        self.middlewares.append(wrapper)
        return wrapper

    def use(self, router: APIRouter, prefix: str = "") -> "APIServer":
        """Chainable method to add a router to the server"""
        for route in router.routes:
            path = prefix + route.path
            self.router.add_route(
                route.method,
                prefix + router.prefix + path,
                route.handler,
                **route.kwargs,
            )

        for path, details in router.openapi["paths"].items():
            path = prefix + path
            self.openapi["paths"][path] = details

        self.openapi["components"]["schemas"].update(
            router.openapi["components"]["schemas"]
        )
        return self
