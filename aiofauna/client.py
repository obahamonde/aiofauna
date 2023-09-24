from __future__ import annotations

import asyncio
import json
import logging
import os
import typing
from functools import wraps
from threading import Lock
from typing import (Any, AsyncGenerator, Dict, List, Literal, Optional, Type,
                    Union)

from aiohttp import ClientResponse, ClientSession, ClientTimeout, TCPConnector
from aiohttp.client_exceptions import (ClientConnectionError,
                                       ClientConnectorSSLError)
from aiohttp.web_exceptions import HTTPException
from dotenv import load_dotenv
from multidict import CIMultiDict
from pydantic import Field

from .api import Client, singleton
from .faunadb.errors import FaunaException
from .faunadb.objects import Expr
from .json import to_json
from .utils import setup_logging

load_dotenv()

Method = Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
Json = Union[Dict[str, Any], List[Dict[str, Any]]]
MaybeJson = Optional[Json]
Headers = Dict[str, str]
MaybeHeaders = Optional[Headers]


class MissingEnvironmentVariable(Exception):
    """Exception for missing environment variable."""

    ...


if "FAUNA_SECRET" not in os.environ:
    raise MissingEnvironmentVariable(
        "The FAUNA_SECRET environment variable is not set."
    )


FAUNA_SECRET = os.environ["FAUNA_SECRET"]
HEADERS = {
    "Authorization": f"Bearer {FAUNA_SECRET}",
    "Content-type": "application/json",
    "Accept": "application/json",
    "User-Agent": "aiofauna-framework",
}

T = typing.TypeVar("T")

logger = setup_logging(__name__)

FAUNA_EXCEPTIONS = (
    HTTPException,
    FaunaException,
    ValueError,
    KeyError,
    TypeError,
    Exception,
    UnicodeError,
    json.JSONDecodeError,
    RuntimeError,
    ClientConnectionError,
    ClientConnectorSSLError,
)


class APIException(HTTPException):
    """Base class for all exceptions raised by an API client."""

    def __init__(self, message: str, status_code: int = 500) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(
            text=json.dumps({"message": message, "status": status_code}),
            content_type="application/json",
        )

class FaunaClient(Client):
    """
    FaunaDB Client

    Args:
        config (APIConfig): APIConfig object
    """
    base_url:str = Field(default="https://db.fauna.com")
    headers: dict[str,str] = Field(default_factory=lambda: HEADERS)


    async def query(self, expr: Expr) -> Any:
        """
        Query FaunaDB
        -----------------
        Args:
            expr (Expr): FaunaDB expression
        Returns:
            Any: FaunaDB response
        """

        response = await self().post("/", data=to_json(expr))
        try:
            data = await response.json()
            if data.get("resource") is not None:
                return data["resource"]
            if data.get("error") is not None:
                return data["error"]
            return data
        except FAUNA_EXCEPTIONS as exc:  # pylint:disable=all
            logger.error(exc.__class__.__name__) # type: ignore
            logger.error(exc)
            raise APIException(str(exc)) from exc