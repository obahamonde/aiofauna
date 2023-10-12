"""REST API Module with automatic OpenAPI generation."""
from inspect import signature
from typing import Any, Callable, Coroutine, Dict, List, Tuple, TypeVar, cast

from aiohttp.typedefs import Handler
from aiohttp.web import Request, RouteDef, RouteTableDef
from typing_extensions import ParamSpec

from ..helpers import do_response
from .docs import extract, load, transform

T = TypeVar("T")
P = ParamSpec("P")


class APIRouter(RouteTableDef):
    """Aiohttp Application with automatic OpenAPI generation."""

    def __init__(self, *, prefix: str = "/", tags: List[str] = [], **kwargs: Any):
        super().__init__(**kwargs)
        self.prefix = prefix
        self.tags = tags
        self.openapi: Dict[str, Any] = {
            "paths": {},
            "components": {"schemas": {}}   
        }
        self._route_open_api_params: Dict[Tuple[str, str], Dict[str, Any]] = {}
        self.routes: List[RouteDef] = []

    def document(self, path: str, method: str):
        """

        Decorator to document a function.

        """

        def decorator(
            func: Callable[P, Coroutine[Any, Any, T]]
        ) -> Callable[P, Coroutine[Any, Any, T]]:
            sig = signature(func)
            params = sig.parameters
            open_api_params = extract(params.copy(), path)
            self._route_open_api_params[(path, method)] = open_api_params
            transform(self.openapi, path, method, func, open_api_params, self.tags)

            async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:  # type: ignore
                assert isinstance(args[0], Request)
                request = args[0]
                args: Any = args[1:]
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
                response = await func(*args, **definitive_args, **kwargs)
                return cast(T, do_response(response))

            wrapper._handler = func  # type: ignore
            wrapper.__name__ = func.__name__
            return wrapper

        return decorator

    def route(self, path: str, method: str, **kwargs: Any):  # type: ignore
        """Decorator to register a new route."""

        def decorator(
            func: Callable[P, Coroutine[Any, Any, T]]
        ) -> Callable[P, Coroutine[Any, Any, T]]:
            route = self.document(self.prefix + path, method)(func)
            self.routes.append(RouteDef(method, path, cast(Handler, route), kwargs))
            return route

        return decorator

    def get(self, path: str, **kwargs: Any):  # type: ignore
        """GET decorator"""

        def decorator(
            func: Callable[P, Coroutine[Any, Any, T]]
        ) -> Callable[P, Coroutine[Any, Any, T]]:
            self.route(path, "GET", **kwargs)(func)
            return func

        return decorator

    def post(self, path: str, **kwargs: Any):  # type: ignore
        """POST decorator"""

        def decorator(
            func: Callable[P, Coroutine[Any, Any, T]]
        ) -> Callable[P, Coroutine[Any, Any, T]]:
            self.route(path, "POST", **kwargs)(func)
            return func

        return decorator

    def put(self, path: str, **kwargs: Any):  # type: ignore
        """PUT decorator"""

        def decorator(
            func: Callable[P, Coroutine[Any, Any, T]]
        ) -> Callable[P, Coroutine[Any, Any, T]]:
            self.route(path, "PUT", **kwargs)(func)
            return func

        return decorator

    def delete(self, path: str, **kwargs: Any):  # type: ignore
        """DELETE decorator"""

        def decorator(
            func: Callable[P, Coroutine[Any, Any, T]]
        ) -> Callable[P, Coroutine[Any, Any, T]]:
            self.route(path, "DELETE", **kwargs)(func)
            return func

        return decorator

    def head(self, path: str, **kwargs: Any):  # type: ignore
        """HEAD decorator"""

        def decorator(
            func: Callable[P, Coroutine[Any, Any, T]]
        ) -> Callable[P, Coroutine[Any, Any, T]]:
            self.route(path, "HEAD", **kwargs)(func)
            return func

        return decorator

    def patch(self, path: str, **kwargs: Any):  # type: ignore
        """PATCH decorator"""

        def decorator(
            func: Callable[P, Coroutine[Any, Any, T]]
        ) -> Callable[P, Coroutine[Any, Any, T]]:
            self.route(path, "PATCH", **kwargs)(func)
            return func

        return decorator

    def options(self, path: str, **kwargs: Any):  # type: ignore
        """OPTIONS decorator"""

        def decorator(
            func: Callable[P, Coroutine[Any, Any, T]]
        ) -> Callable[P, Coroutine[Any, Any, T]]:
            self.route(path, "OPTIONS", **kwargs)(func)
            return func

        return decorator
