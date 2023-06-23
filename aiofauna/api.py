"""REST API Module with automatic OpenAPI generation."""
import asyncio
import os
from functools import wraps
from inspect import signature
from typing import Awaitable, Callable

from aiohttp.typedefs import Handler
from aiohttp.web import (Application, Request, Response, StreamResponse,
                         json_response, run_app)
from aiohttp.web_exceptions import HTTPException
from aiohttp.web_middlewares import middleware
from aiohttp.web_ws import WebSocketResponse
from aiohttp_sse import EventSourceResponse, sse_response

from .docs import extract, html, load, transform
from .helpers import do_response
from .json import jsonable_encoder

Middleware = Callable[[Request, Handler], Awaitable[StreamResponse]]

class Api(Application):
    """Aiohttp Application with automatic OpenAPI generation."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.openapi = {
            "openapi": "3.0.0",
            "info": {"title": "AioFauna", "version": "1.0.0"},
            "paths": {},
            "components": {"schemas": {}},
            "description": "AioFauna API",
        }
        self._route_open_api_params = {}

        @self.get("/openapi.json")
        async def openapi():
            response = jsonable_encoder(self.openapi)
            return json_response(response)

        @self.get("/docs")
        async def docs():
            return Response(text=html, content_type="text/html")

    def document(self, path: str, method: str):
        """

        Decorator to document a function.

        """

        def decorator(func):
            sig = signature(func)
            params = sig.parameters
            open_api_params = extract(params.copy(), path)
            self._route_open_api_params[(path, method)] = open_api_params
            transform(self.openapi, path, method, func, open_api_params)

            async def wrapper(*args, **kwargs):
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
            func.injectable = True
            wrapper._handler = func
            return wrapper

        return decorator

    def get(self, path: str, **kwargs):
        """GET decorator"""

        def decorator(func):
            self.router.add_get(path, self.document(path, "GET")(func), **kwargs)
            return func

        return decorator

    def post(self, path: str, **kwargs):
        """POST decorator"""

        def decorator(func):
            self.router.add_post(path, self.document(path, "POST")(func), **kwargs)
            return func

        return decorator

    def put(self, path: str, **kwargs):
        """PUT decorator"""

        def decorator(func):
            self.router.add_put(path, self.document(path, "PUT")(func), **kwargs)
            return func

        return decorator

    def delete(self, path: str, **kwargs):
        """DELETE decorator"""

        def decorator(func):
            self.router.add_delete(path, self.document(path, "DELETE")(func), **kwargs)
            return func

        return decorator

    def patch(self, path: str, **kwargs):
        """PATCH decorator"""

        def decorator(func):
            self.router.add_patch(path, self.document(path, "PATCH")(func), **kwargs)
            return func

        return decorator

    def head(self, path: str, **kwargs):
        """HEAD decorator"""

        def decorator(func):
            self.router.add_head(path, self.document(path, "HEAD")(func), **kwargs)
            return func

        return decorator

    def options(self, path: str, **kwargs):
        """OPTIONS decorator"""

        def decorator(func):
            self.router.add_options(
                path, self.document(path, "OPTIONS")(func), **kwargs
            )
            return func

        return decorator

    def on_event(self, event: str):
        """On event handler"""

        def decorator(func):
            if event not in ("startup", "shutdown"):
                raise ValueError("Event must be startup or shutdown")
            elif event == "startup":
                self.on_startup.append(func)
            else:
                self.on_shutdown.append(func)
            return func

        return decorator

    def sse(self, path: str) -> Callable:  # pylint: disable=invalid-name
        """Server-Sent Events decorator"""

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def wrapper(request: Request)->EventSourceResponse:
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

    def websocket(self, path: str) -> Callable:  # pylint: disable=invalid-name
        """Websocket decorator"""

        def decorator(func: Callable) -> Callable:
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

    def use(self, prefix, api):
        if not isinstance(api, Api):
            raise TypeError(str(api) + " is not an Api instance")
        if not prefix.startswith("/"):
            prefix = "/" + prefix
        if not prefix.endswith("/"):
            prefix += "/"
        api.prefix = prefix
        self.add_subapp(prefix, api)
        self.openapi["paths"].update(api.openapi["paths"])
        self.openapi["components"]["schemas"].update(
            api.openapi["components"]["schemas"]
        )
        self.openapi["components"]["securitySchemes"].update(
            api.openapi["components"]["securitySchemes"]
        )
        self.openapi["components"]["responses"].update(
            api.openapi["components"]["responses"]
        )

    def static(self):
        """Static folder creation and serving"""
        try:
            os.makedirs("static", exist_ok=True)
        except OSError:
            pass
        try:
            os.makedirs("static/docs", exist_ok=True)
        except OSError:
            pass
        self.router.add_static("/", "static")
        @self.get("/")
        def index():
            return Response(
                    text=open("static/index.html", "r").read(),
                    content_type="text/html",
                )
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
    

    def run(self, host: str = "0.0.0.0", port=8080):
        run_app(self, host=host, port=port)