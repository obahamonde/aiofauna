"""
Helper functions for aiofauna.
"""
import asyncio
import functools
import typing
from concurrent.futures import ProcessPoolExecutor
from functools import singledispatch
from typing import Any, List, Union

from aiohttp.web import Response, json_response
from pydantic import BaseModel  # pylint: disable=no-name-in-module
from typing_extensions import ParamSpec
from .json import to_json
from .odm import FaunaModel


T = typing.TypeVar("T")
P = ParamSpec("P")

def async_io(
    func: typing.Callable[P, T]
) -> typing.Callable[P, typing.Coroutine[T, Any, Any]]:
    """
    Decorator to convert an IO bound function to a coroutine by running it in a thread pool.
    """

    @functools.wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        return await asyncio.to_thread(func, *args, **kwargs)

    return wrapper


def async_cpu(
    func: typing.Callable[P, T]
) -> typing.Callable[P, typing.Coroutine[T, Any, Any]]:
    """
    Decorator to convert a CPU bound function to a coroutine by running it in a process pool.
    """

    @functools.wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        with ProcessPoolExecutor() as pool:
            try:
                return await asyncio.get_running_loop().run_in_executor(
                    pool, func, *args, **kwargs
                )
            except RuntimeError:
                return await asyncio.get_event_loop().run_in_executor(
                    pool, func, *args, **kwargs
                )

    return wrapper


@singledispatch
def do_response(response: T) -> Response:
    """
    Process the response from a view function and return an aiohttp.web.Response object.
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
    return Response(
        status=200, body=response, content_type="application/octet-sse_stream"
    )


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
    return json_response(response, dumps=to_json)


@do_response.register(tuple)
def _(response: tuple) -> Response:
    return do_response(list(response))


@do_response.register(set)
def _(response: set) -> Response:
    return do_response(list(response))


@do_response.register(frozenset)
def _(response: frozenset) -> Response:
    return do_response(list(response))


@do_response.register(type(None))
def _(response: None) -> Response:
    return Response(status=200, text="", content_type="text/plain")


@do_response.register(Response)
def _(response: Response) -> Response:
    return response
