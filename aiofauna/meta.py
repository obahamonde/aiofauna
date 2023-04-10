import asyncio
from typing import (
    Awaitable,
    AsyncGenerator,
    Callable,
    Coroutine,
    Dict,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
)
from functools import singledispatch, wraps
import jinja2
from pydantic import BaseModel
from aiofauna.odm import AsyncFaunaModel
from aiohttp.web import Response, json_response
from jinja2 import Template


@singledispatch
def parse_to_response(obj):
    return obj


@parse_to_response.register(BaseModel)
def _(obj):
    return json_response(obj.dict())


@parse_to_response.register(AsyncFaunaModel)
def _(obj):
    return json_response(obj.dict())


@parse_to_response.register(dict)
def _(obj):
    return json_response(obj)


@parse_to_response.register(list)
def _(obj):
    return json_response(obj)


@parse_to_response.register(str)
def _(obj):
    return Response(text=obj, content_type="text/plain")


@parse_to_response.register(jinja2.Template)
def _(obj):
    return Response(text=obj.render(), content_type="text/html")


def return_response(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Response:
        if asyncio.iscoroutinefunction(func):
            return parse_to_response(await func(*args, **kwargs))
        return parse_to_response(func(*args, **kwargs))

    return wrapper
