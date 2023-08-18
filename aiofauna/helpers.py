"""
Flaskaesque helper functions for aiohttp.
"""
import asyncio
import functools
import json
import types
import typing
from concurrent.futures import ProcessPoolExecutor
from functools import singledispatch
from typing import Any, List, Union

from aiohttp.web import HTTPException, Request, Response, json_response
from pydantic import BaseModel  # pylint: disable=no-name-in-module
from typing_extensions import ParamSpec

from aiofauna.json import FaunaJSONEncoder

from .json import parse_json, to_json
from .odm import FaunaModel

T = typing.TypeVar("T")
P = ParamSpec("P")


def async_io(func: typing.Callable[P, T]) -> typing.Callable[P, typing.Awaitable[T]]:
    """
    Decorator to make a function async.
    """

    @functools.wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> typing.Any:
        return await asyncio.to_thread(func, *args, **kwargs)

    return wrapper


def async_cpu(func: typing.Callable[P, T]) -> typing.Callable[P, typing.Awaitable[T]]:
    """
    Decorator to make a function async.
    """

    @functools.wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> typing.Any:
        with ProcessPoolExecutor() as pool:
            return await asyncio.get_running_loop().run_in_executor(
                pool, func, *args, **kwargs
            )

    return wrapper


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
    return json_response([x for x in response], dumps=to_json)
