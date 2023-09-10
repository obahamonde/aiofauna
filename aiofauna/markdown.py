"""Markdown component decorator for Jinja2 templates."""
import jinja2
import typing_extensions
import typing
from typing import Any, Callable, Coroutine
import functools
from .utils import render_markdown

T = typing.TypeVar("T")
P = typing_extensions.ParamSpec("P")


def md_component(dir: str = "docs", file: str = "base.j2"):
    def decorator(
        func: Callable[P, Coroutine[Any, Any, T]]
    ) -> Callable[P, Coroutine[Any, Any, T]]:
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(dir),
            autoescape=jinja2.select_autoescape(["html", "xml"]),
            enable_async=True,
        )
        md = render_markdown(func.__doc__)
        template_str = env.from_string(
            """{% extends """
            + "'"
            + file
            + "'"
            + """ %} {% block content %}"""
            + md
            + """{% endblock %}"""
        )

        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            return await template_str.render_async(**kwargs)

        return wrapper

    return decorator
