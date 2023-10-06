from __future__ import annotations

import json
import os
import typing
from typing import Any

from aiohttp.client_exceptions import ClientConnectionError, ClientConnectorSSLError
from aiohttp.web_exceptions import HTTPException
from dotenv import load_dotenv
from pydantic import Field

from ..data.json import to_json
from ..faunadb.errors import FaunaException
from ..faunadb.objects import Expr
from ..utils import setup_logging
from .api_client import Client

load_dotenv()


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
    """
    API Exception
    -------------
    Args:
        message (str): Error message
        status_code (int, optional): HTTP status code. Defaults to 500.

    Raises:
        HTTPException: HTTP Exception
    """

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
    --------------

    The main client for interacting with FaunaDB. This client is used to query the database and perform transactions on top of `FQL <https://docs.fauna.com/fauna/current/api/fql/>` language through a friendly pythonic interface.

    Args:
        base_url (str, optional): Base URL for the client. Defaults to "https://db.fauna.com".

    Attributes:
        base_url (str): Base URL for the client.
        headers (dict[str, str]): Headers for the client.

    """

    base_url: str = Field(default="https://db.fauna.com")
    headers: dict[str, str] = Field(default_factory=lambda: HEADERS)

    async def query(self, expr: Expr) -> Any:
        """
        Query FaunaDB
        -----------------
        Args:
            expr (Expr): FaunaDB expression

            A FaunaDB expression is a JSON object that represents a FaunaDB query. For more information on FaunaDB expressions, see the `FQL <https://docs.fauna.com/fauna/current/api/fql/>`_ documentation.

            Basically an `Expr` is a `Ref`, `SetRef` or `FaunaTime` object, wrapping a JSON object that contains a FaunaDB query.

        Returns:

            The result of the query.

        Raises:

            APIException: API Exception

        Example:

            .. code-block:: python

                from aiofauna import FaunaClient
                from aiofauna.data import query

                client = FaunaClient()

                await client.query(q.create_database({"name": "my_database"}))
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
            logger.error(exc.__class__.__name__)  # type: ignore
            logger.error(exc)
            raise APIException(str(exc)) from exc
