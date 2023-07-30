from __future__ import annotations

import asyncio
import json
import logging
import os
import typing
from dataclasses import dataclass, field
from functools import wraps
from re import T
from threading import Lock
from typing import (Any, AsyncGenerator, Dict, List, Literal, NamedTuple,
                    Optional, Type, Union)

from aiohttp import (ClientConnectionError, ClientConnectorSSLError,
                     ClientResponse, ClientSession, ClientTimeout,
                     TCPConnector)
from aiohttp.web_exceptions import HTTPException
from dotenv import load_dotenv
from multidict import CIMultiDict
from pydantic import BaseModel

from .faunadb.errors import FaunaException
from .faunadb.objects import Expr
from .json import FaunaJSONEncoder, to_json
from .logging import setup_logging
from .typedefs import LazyProxy

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
}

T = typing.TypeVar("T")

logger = setup_logging(__name__)


def singleton(cls: typing.Type[T]) -> typing.Callable[..., T]:  # type: ignore
    instance = None
    lock = Lock()

    @wraps(cls)
    def wrapper(*args, **kwargs):
        nonlocal instance
        if instance is None:
            with lock:
                if instance is None:
                    instance = cls(*args, **kwargs)
        return instance

    return wrapper


class APIException(HTTPException):
    """Base class for all exceptions raised by an API client."""

    def __init__(self, message: str, status_code: int = 500) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(
            text=json.dumps({"message": message, "status": status_code}),
            content_type="application/json",
        )


@dataclass(frozen=True)
class ConnectorConfig:
    ssl: bool = field(default=False)
    limit: int = field(default=1000)
    keepalive_timeout: int = field(default=10)


@dataclass(init=True, repr=True, unsafe_hash=False, frozen=False)
class APIConfig:
    base_url: str
    headers: Headers
    logger: logging.Logger = field(default=setup_logging(__name__))
    exception_class: Type[HTTPException] = field(default=APIException)
    session: Optional[ClientSession] = field(default=None)
    connector_config: ConnectorConfig = field(default_factory=ConnectorConfig)
    read_bufsize: int = field(default=2**16)
    connector_owner: bool = field(default=True)
    trust_env: bool = field(default=True)


@singleton
@dataclass(init=True, repr=True, unsafe_hash=False, frozen=False)
class FaunaClient(LazyProxy[ClientSession]):
    """
    FaunaDB Client

    Args:
        config (APIConfig): APIConfig object
    """

    config: APIConfig = APIConfig(
        base_url="https://db.fauna.com",
        headers=HEADERS,
        logger=setup_logging(__name__),
        exception_class=APIException,
        session=None,
        connector_config=ConnectorConfig(),
    )
    session_creation_lock = asyncio.Lock()

    def __load__(self) -> ClientSession:
        if self.config.session is None:
            return ClientSession(
                "https://db.fauna.com",
                headers=CIMultiDict(self.config.headers),  # type: ignore
                connector=TCPConnector(
                    keepalive_timeout=self.config.connector_config.keepalive_timeout,
                    ssl=self.config.connector_config.ssl,
                    limit=self.config.connector_config.limit,
                ),
                connector_owner=self.config.connector_owner,
                trust_env=self.config.trust_env,
                read_bufsize=self.config.read_bufsize,
            )
        return self.config.session

    async def query(self, expr: Expr) -> Any:
        async with self.session_creation_lock:
            if self.config.session is None:
                self.config.session = self.__load__()
        session = self.config.session
        async with session.post(
            "/",
            data=to_json(expr),
        ) as response:
            try:
                data = await response.json()
                self.config.logger.info(data)
                if data.get("resource") is not None:
                    return data["resource"]
                if data.get("error") is not None:
                    return data["error"]
                return data

            except (
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
            ) as exc:  # pylint:disable=all
                self.config.logger.error(exc)
                raise self.config.exception_class from exc

    async def stream(self, expr: Expr) -> AsyncGenerator[str, None]:
        session = self.__load__()
        async with session.post(
            "",
            data=to_json(expr),
            headers={
                "Authorization": f"Bearer {self.secret}",
                "Content-type": "application/json",
                "Accept": "text/event-stream",
                "Keep-Alive": "timeout=5, max=900",
                "Connection": "keep-alive",
                "Cache-Control": "no-cache",
                "X-Last-Seen-Txn": "0",
                "X-Request-By": "aiofauna",
                "X-Query-By": "@obahamonde",
            },
        ) as response:
            async for chunk in response.content.iter_any():
                try:
                    yield chunk.decode()
                except (
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
                ) as exc:
                    self.config.logger.error(exc)
                    yield str(exc)

    async def cleanup(self):
        if self.config.session is not None:
            await self.config.session.close()

    def __del__(self):
        asyncio.run(self.cleanup())


@dataclass(init=True, repr=True, unsafe_hash=False, frozen=False)
class APIClient(LazyProxy[ClientSession]):
    """
    Generic HTTP Client
    """

    base_url: str = field(init=True, repr=True)
    headers: Dict[str, str] = field(default_factory=dict)
    _subclasses: Optional[List[Type[APIClient]]] = None
    _session_creation_lock = asyncio.Lock()
    _session: Optional[ClientSession] = None

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls._subclasses is None:
            cls._subclasses = []
        cls._subclasses.append(cls)

    @classmethod
    async def cleanup(cls):
        if hasattr(cls, "_subclasses") and cls._subclasses is not None:
            tasks = []
            for subclass in cls._subclasses:
                if subclass._session is not None:
                    tasks.append(subclass._session.close())
            await asyncio.gather(*tasks)

    async def __load__(self) -> ClientSession:
        logger.info("Loading session for %s", self.base_url)
        async with self._session_creation_lock:
            if self._session is None:
                self._session = ClientSession(
                    self.base_url,
                    headers=CIMultiDict(self.headers),
                    response_class=ClientResponse,
                    connector=TCPConnector(
                        keepalive_timeout=30,
                        ssl=False,
                        limit=10000,
                    ),
                )
        return self._session

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.base_url}>"

    async def fetch(
        self,
        url: str,
        method: Method = "GET",
        json: MaybeJson = None,
    ):
        session = await self.__load__()
        async with session.request(
            method, url, headers=self.headers, json=json
        ) as response:
            logger.info("Fetching JSON from %s with method %s", url, method)
            try:
                return await response.json()
            except (
                HTTPException,
                FaunaException,
                ValueError,
                KeyError,
                TypeError,
                Exception,
            ) as exc:  # pylint:disable=broad-exception-caught, unused-variable
                logger.error(exc)
                raise APIException(str(exc)) from exc

    async def text(self, url: str, method: Method = "GET", json: MaybeJson = None):
        session = await self.__load__()
        async with session.request(
            method, url, headers=self.headers, json=json
        ) as response:
            logger.info("Fetching Text from %s with method %s", url, method)
            try:
                return await response.text()
            except (
                HTTPException,
                FaunaException,
                ValueError,
                KeyError,
                TypeError,
                Exception,
            ) as exc:  # pylint:disable=broad-exception-caught, unused-variable
                logger.error(exc)
                raise APIException(str(exc)) from exc

    async def stream(
        self,
        url: str,
        method: Method = "GET",
        json: MaybeJson = None,
    ):
        session = await self.__load__()
        async with session.request(
            method, url, headers=self.headers, json=json
        ) as response:
            logger.info("Streaming from %s with method %s", url, method)
            async for chunk in response.content.iter_any():
                try:
                    yield chunk.decode()
                except (
                    HTTPException,
                    FaunaException,
                    ValueError,
                    KeyError,
                    TypeError,
                    Exception,
                ) as exc:
                    logger.error(exc)
                    yield str(exc)
                    raise APIException(str(exc)) from exc

    async def get(self, url: str):
        return await self.fetch(url=url, method="GET")

    async def post(self, url: str, json: MaybeJson = None):
        return await self.fetch(url=url, method="POST", json=json)

    async def put(self, url: str, json: MaybeJson = None):
        return await self.fetch(url=url, method="PUT", json=json)

    async def patch(self, url: str, json: MaybeJson = None):
        return await self.fetch(url=url, method="PATCH", json=json)

    async def delete(self, url: str, json: MaybeJson = None):
        return await self.fetch(url=url, method="DELETE", json=json)

    def update_headers(self, headers: Dict[str, str]):
        """
        Update the headers used by this API client.

        Returns:
            self: Allows method chaining.
        """
        self.headers.update(headers)
        logger.info("Updated headers %s", self.headers)
        return self


def make_client(name: str, base_url: str, headers: Dict[str, str]) -> Type[APIClient]:
    """
    Create a new API client class.

    Args:
        name: The name of the client.
        base_url: The base URL for the client.
        headers: The headers to use for the client.

    Returns:
        A new API client class.
    """
    return type(
        name,
        (APIClient,),
        {
            "base_url": base_url,
            "headers": headers,
        },
    )
