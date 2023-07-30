"""
Flaskaesque helper functions for aiohttp.
"""
import asyncio
import functools
import json
import types
import typing
from concurrent.futures import ThreadPoolExecutor
from functools import singledispatch
from typing import Any, List, Union

from aiohttp.web import HTTPException, Request, Response, json_response

from aiofauna.json import FaunaJSONEncoder

from .json import parse_json, to_json
from .odm import BaseModel, FaunaModel

T = typing.TypeVar("T")


def asyncify(
    func: typing.Callable[..., typing.Any],
) -> typing.Callable[..., typing.Awaitable[typing.Any]]:
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        bound = functools.partial(func, self, *args, **kwargs)
        if asyncio.get_event_loop().is_running():
            loop = asyncio.get_event_loop()
            return loop.run_in_executor(self.executor, bound)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_in_executor(self.executor, bound)

    return typing.cast(typing.Callable[..., typing.Awaitable[typing.Any]], wrapper)


def aio(max_workers: int = 5) -> typing.Callable[[typing.Type], typing.Type]:
    """Decorator that converts all the methods of a class into async methods."""

    def decorator(cls: typing.Type) -> typing.Type:
        attrs: typing.Dict[str, typing.Any] = {}
        attrs["executor"] = ThreadPoolExecutor(max_workers=max_workers)
        for attr_name, attr_value in cls.__dict__.items():
            if (
                isinstance(attr_value, types.FunctionType)
                and attr_name.startswith("__") is False
            ):
                attrs[attr_name] = asyncify(attr_value)
            else:
                attrs[attr_name] = attr_value
        return type(cls.__name__, cls.__bases__, attrs)

    return decorator


@singledispatch
def do_response(response: Any) -> Response:
    """
    Flask-esque function to make a response from a function.
    """
    return response


@do_response.register(BaseModel)
def _(response: BaseModel) -> Response:
    return json_response(response.dict(exclude_none=True), dumps=to_json)

@do_response.register(FaunaModel)
def _(response: FaunaModel) -> Response:
    return json_response(response.dict(), dumps=to_json)


@do_response.register(dict)
def _(response: dict) -> Response:
    return json_response(response, dumps=to_json)


@do_response.register(str)
def _(response: str) -> Response:
    if response.startswith("<") and response.endswith(">"):
        return Response(status=200, text=response, content_type="text/html")
    return Response(status=200, text=response, content_type="text/plain")

@do_response.register(bytes)
def _(response: bytes) -> Response:
    return Response(status=200, body=response, content_type="application/octet-stream")


@do_response.register(int)
def _(response: int) -> Response:
    return Response(status=200, text=str(response), content_type="text/plain")


@do_response.register(float)
def _(response: float) -> Response:
    return Response(status=200, text=str(response), content_type="text/plain")


@do_response.register(bool)
def _(response: bool) -> Response:
    return Response(status=200, text=str(response), content_type="text/plain")


@do_response.register(list)
def _(response: List[Union[FaunaModel, BaseModel, dict, str, int, float]]) -> Response:
    return json_response(
        [x for x in response], dumps=to_json
    )
    
