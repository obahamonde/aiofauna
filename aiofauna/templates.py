import asyncio
import functools
from typing import Any, Callable, Coroutine, Dict, Type, TypeVar

from jinja2 import Environment, FileSystemLoader, Template
from pydantic import BaseModel  # pylint: disable=no-name-in-module
from typing_extensions import ParamSpec

T = TypeVar("T", bound=BaseModel)
P = ParamSpec("P")


def docstring(
    cls: Type[T],
) -> Callable[
    [Callable[..., Coroutine[Any, Any, Dict[str, Any]]]],
    Callable[..., Coroutine[Any, Any, str]],
]:
    def decorator(
        func: Callable[..., Coroutine[Any, Any, Dict[str, Any]]]
    ) -> Callable[..., Coroutine[Any, Any, str]]:
        async def wrapper(*args: Any, **kwargs: Any) -> str:
            if cls.__doc__ is None:
                raise ValueError("Component must have a docstring")
            template = Template(cls.__doc__)
            context = await func(*args, **kwargs)
            model_instance = cls(**context)
            return template.render(**model_instance.dict())

        return wrapper

    return decorator


def page(
    cls: Type[T], template: str, template_dir: str = "pages"
) -> Callable[
    [Callable[P, Coroutine[Any, Any, Dict[str, Any]]]],
    Callable[P, Coroutine[Any, Any, str]],
]:
    environment = Environment(loader=FileSystemLoader(template_dir), enable_async=True)

    class Decorator:
        def __call__(
            self, func: Callable[P, Coroutine[Any, Any, Dict[str, Any]]]
        ) -> Callable[P, Coroutine[Any, Any, str]]:
            @functools.wraps(func)
            async def wrapper(*args: P.args, **kwargs: P.kwargs) -> str:
                template_object = environment.get_template(template)
                context = await func(*args, **kwargs)
                model_instance = cls(**context)
                if asyncio.iscoroutinefunction(func):
                    return await template_object.render_async(**model_instance.dict())
                return template_object.render(**model_instance.dict())

            return wrapper

    return Decorator()


def component(
    cls: Type[T], template: str, template_dir: str = "components"
) -> Callable[
    [Callable[P, Coroutine[Any, Any, Dict[str, Any]]]],
    Callable[P, Coroutine[Any, Any, str]],
]:
    environment = Environment(loader=FileSystemLoader(template_dir), enable_async=True)

    class Decorator:
        def __call__(
            self, func: Callable[P, Coroutine[Any, Any, Dict[str, Any]]]
        ) -> Callable[P, Coroutine[Any, Any, str]]:
            @functools.wraps(func)
            async def wrapper(*args: P.args, **kwargs: P.kwargs) -> str:
                template_object = environment.get_template(template)
                context = await func(*args, **kwargs)
                model_instance = cls(**context)
                if asyncio.iscoroutinefunction(func):
                    return await template_object.render_async(**model_instance.dict())
                return template_object.render(**model_instance.dict())

            return wrapper

    return Decorator()
