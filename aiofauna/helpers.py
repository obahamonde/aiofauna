"""
Flaskaesque helper functions for aiohttp.
"""
import json
from functools import singledispatch
from typing import Any, List, Union

from aiohttp import web
from aiohttp.web import Response

from .odm import BaseModel, FaunaModel


def redirect(url):
    """
    Create an HTTP redirect response.

    Args:
        url (str): The URL to redirect to.

    Returns:
        web.HTTPFound: An HTTP redirect response with the specified URL.
    """

    return web.HTTPFound(url)


def make_response(data, headers=None, status=200):
    """
    Create an HTTP response with the given data, headers, and status code.

    Args:
        data (str): The response body data.
        headers (dict, optional): A dictionary of headers to include in the response. Defaults to None.
        status (int, optional): The HTTP status code for the response. Defaults to 200.

    Returns:
        web.Response: An HTTP response with the specified data, headers, and status code.
    """
    return web.Response(body=data, headers=headers, status=status)

@singledispatch
def do_response(response: Any) -> Response:
    """
    Flask-esque function to make a response from a function.
    """
    return response


@do_response.register(BaseModel)
def _(response: BaseModel) -> Response:
    return Response(
        status=200, body=response.json(
            exclude_none=True
            ), content_type="application/json"
    )


@do_response.register(FaunaModel)
def _(response: FaunaModel) -> Response:
    return Response(
        status=200, text=response.json(
            exclude_none=True
            ), content_type="application/json"
    )


@do_response.register(dict)
def _(response: dict) -> Response:
    return Response(
        status=200, body=json.dumps(response), content_type="application/json"
    )


@do_response.register(str)
def _(response: str) -> Response:
    if "<html>" in response:
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
    processed_response = []

    for item in response:
        if isinstance(item, (FaunaModel, BaseModel)):
            processed_response.append(item.json(exclude_none=True))
        elif isinstance(item, dict):
            processed_response.append(item)
        elif isinstance(item, str):
            processed_response.append(item)
        elif isinstance(item, (int, float, bool)):
            processed_response.append(str(item))
        else:
            raise TypeError(f"Cannot serialize type {type(item)}")
    return Response(
        status=200, body=json.dumps(processed_response), content_type="application/json"
    )