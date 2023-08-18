"""REST API Module with automatic OpenAPI generation."""
from __future__ import annotations

import asyncio
from functools import wraps
from inspect import signature
from typing import Awaitable, Callable, List

from aiohttp.typedefs import Handler
from aiohttp.web import Request, RouteDef, RouteTableDef, StreamResponse
from aiohttp.web_ws import WebSocketResponse
from aiohttp_sse import EventSourceResponse, sse_response

from .docs import extract, load, transform
from .helpers import do_response

Middleware = Callable[[Request, Handler], Awaitable[StreamResponse]]


class APIRouter(RouteTableDef):
    """Aiohttp Application with automatic OpenAPI generation."""

    def __init__(self, *args, prefix: str = "", tags: List[str] = [], **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = prefix
        self.tags = tags
        self.openapi = {
            "paths": {},
            "components": {"schemas": {}},
            "tags": [{"name": tag} for tag in tags if tag],
        }
        self._route_open_api_params = {}
        self.routes: List[RouteDef] = []

    def document(self, path: str, method: str):
        """

        Decorator to document a function.

        """

        def decorator(func: Handler):
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

    def route(self, path: str, method: str):
        """Decorator to register a new route."""

        def decorator(func: Handler, **kwargs):
            route = self.document(self.prefix + path, method)(func)
            self.routes.append(RouteDef(method, path, route, kwargs))
            return route

        return decorator

    def get(self, path: str, **kwargs) -> Callable[[Handler], Handler]:
        """GET decorator"""

        def decorator(func: Handler):
            self.route(path, "GET", **kwargs)(func)
            return func

        return decorator

    def post(self, path: str, **kwargs) -> Callable[[Handler], Handler]:
        """POST decorator"""

        def decorator(func: Handler):
            self.route(path, "POST", **kwargs)(func)
            return func

        return decorator

    def put(self, path: str, **kwargs) -> Callable[[Handler], Handler]:
        """PUT decorator"""

        def decorator(func: Handler):
            self.route(path, "PUT", **kwargs)(func)
            return func

        return decorator

    def delete(self, path: str, **kwargs) -> Callable[[Handler], Handler]:
        """DELETE decorator"""

        def decorator(func: Handler):
            self.route(path, "DELETE", **kwargs)(func)
            return func

        return decorator

    def patch(self, path: str, **kwargs) -> Callable[[Handler], Handler]:
        """PATCH decorator"""

        def decorator(func: Handler):
            self.route(path, "PATCH", **kwargs)(func)
            return func

        return decorator

    def head(self, path: str, **kwargs) -> Callable[[Handler], Handler]:
        """HEAD decorator"""

        def decorator(func: Handler):
            self.route(path, "HEAD", **kwargs)(func)
            return func

        return decorator

    def sse(self, path: str) -> Callable:  # pylint: disable=invalid-name
        """Server-Sent Events decorator"""

        def decorator(func: Callable) -> Callable:
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

            self.route(path, "GET")(wrapper)
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

            self.route(path, wrapper)
            return wrapper

        return decorator
