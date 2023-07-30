from __future__ import annotations

import functools
import json
import types
from typing import *

from aiohttp.web import HTTPException, Request, Response
from jinja2 import Environment, FileSystemLoader, Template, select_autoescape
from jinja2.exceptions import (TemplateAssertionError, TemplateError,
                               TemplateNotFound, TemplateSyntaxError,
                               UndefinedError)
from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module
from typing_extensions import ParamSpec

from .logging import setup_logging

logger = setup_logging(__name__)

Res = TypeVar("Res", bound=Response)
Req = TypeVar("Req", bound=Request)
Exc = TypeVar("Exc", bound=HTTPException)
View = Callable[[Req], Awaitable[Res]]
P = ParamSpec("P")
V = TypeVar("V", bound=View)
T = TypeVar("T")


class HTMLResponse(Response):
    def __init__(self, text: str, status: int = 200, **kwargs: Any) -> None:
        super().__init__(text=text, status=status, **kwargs)
        self.headers["Content-Type"] = "text/html"
        self.content_type = "text/html"


class JSONResponse(Response):
    def __init__(self, data: Any, status: int = 200, **kwargs: Any) -> None:
        super().__init__(text=json.dumps(data, indent=4), status=status, **kwargs)
        self.headers["Content-Type"] = "application/json"
        self.content_type = "application/json"


class PlainTextResponse(Response):
    def __init__(self, text: str, status: int = 200, **kwargs: Any) -> None:
        super().__init__(text=text, status=status, **kwargs)
        self.headers["Content-Type"] = "text/plain"
        self.content_type = "text/plain"


jinja_env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(["html", "xml"]),
    enable_async=True,
)


async def render_template(template_name: str, context: Dict[str, Any]) -> HTMLResponse:
    """
    Renders a template and returns a response.
    """
    try:
        template_ = jinja_env.get_template(template_name)
        html = await template_.render_async(**context)
        return HTMLResponse(html)
    except (
        TemplateError,
        TemplateAssertionError,
        TemplateSyntaxError,
        TemplateNotFound,
        UndefinedError,
    ) as e:
        logger.error(e)
        raise HTTPException(reason=str(e)) from e


async def render_template_string(
    template_string: str, context: Dict[str, Any]
) -> HTMLResponse:
    """
    Renders a template and returns a response.
    """
    try:
        template_ = Template(template_string)
        html = await template_.render_async(**context)
        return HTMLResponse(html)
    except (
        TemplateError,
        TemplateAssertionError,
        TemplateSyntaxError,
        TemplateNotFound,
        UndefinedError,
    ) as e:
        logger.error(e)
        raise HTTPException(reason=str(e)) from e


def template(
    template_name: str, func: Callable[[Request], Awaitable[Dict[str, Any]]]
) -> Callable[[Request], Awaitable[HTMLResponse]]:
    """
    Decorator to render a template and return a response.
    """

    @functools.wraps(func)
    async def wrapper(request: Request) -> HTMLResponse:
        try:
            template_ = jinja_env.get_template(template_name)
            context = await func(request)
            html = await template_.render_async(**context)
            return HTMLResponse(html)
        except (
            TemplateError,
            TemplateAssertionError,
            TemplateSyntaxError,
            TemplateNotFound,
            UndefinedError,
        ) as e:
            logger.error(e)
            raise HTTPException(reason=str(e)) from e

    return wrapper
