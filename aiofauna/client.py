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

# Load environment variables once at the start of the program
FAUNA_SECRET = os.environ["FAUNA_SECRET"]
HEADERS = {
    "Authorization": f"Bearer {FAUNA_SECRET}",
    "Content-type": "application/json",
    "Accept": "application/json"
}

T = typing.TypeVar("T")

def singleton(cls: typing.Type[T]) -> typing.Callable[..., T]: # type: ignore
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
        super().__init__(text=json.dumps({"message": message, "status": status_code}),content_type="application/json")

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
    timeout:int = field(default=10)
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
        connector_config=ConnectorConfig()
    )
    
    
        
    def __load__(self) -> ClientSession:
        if self.config.session is None:
            return ClientSession(
                "https://db.fauna.com",
                headers=CIMultiDict(self.config.headers), # type: ignore
                connector=TCPConnector(
                keepalive_timeout=self.config.connector_config.keepalive_timeout,           
                ssl=self.config.connector_config.ssl,
                limit=self.config.connector_config.limit,
                ),  
                timeout=ClientTimeout(total=self.config.timeout),
                connector_owner=self.config.connector_owner,
                trust_env=self.config.trust_env,
                read_bufsize=self.config.read_bufsize,
            )
        return self.config.session
    
    async def query(self, expr: Expr) -> Any:
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
                    ClientConnectorSSLError
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
                    ClientConnectorSSLError
                ) as exc:
                    self.config.logger.error(exc)
                    yield str(exc)
       
    async def cleanup(self):
        if self.config.session is not None:
            await self.config.session.close()
            
@dataclass(init=True, repr=True, unsafe_hash=False, frozen=False)
class ApiClient(LazyProxy[ClientSession]):
    """
    Generic HTTP Client
    """
    config: APIConfig
    subclasses: Optional[List[Type[ApiClient]]]
    
    @classmethod    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.subclasses is None:
            cls.subclasses = []
        cls.subclasses.append(cls)
        
    @classmethod
    async def cleanup(cls):
        if hasattr(cls, "subclasses") and cls.subclasses is not None:
            tasks = []
            for subclass in cls.subclasses:
                if subclass.config.session is not None:
                    tasks.append(subclass.config.session.close())
            await asyncio.gather(*tasks)
    
    def __load__(self) -> ClientSession:
        if self.config.session is None:
            self.config.session = ClientSession(
                self.config.base_url,
                headers=CIMultiDict(self.config.headers), 
                response_class=ClientResponse,
                connector=TCPConnector(
                    keepalive_timeout=self.config.connector_config.keepalive_timeout,           
                    ssl=self.config.connector_config.ssl,
                    limit=self.config.connector_config.limit,
                ),  
                timeout=ClientTimeout(total=self.config.timeout),
                connector_owner=self.config.connector_owner,
                trust_env=self.config.trust_env,
                read_bufsize=self.config.read_bufsize,
            )
        return self.config.session

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.config.base_url}>"
            
    async def fetch(
        self,
        url: str,
        method: Method = "GET",
        json: MaybeJson = None):
        session = self.__load__()
        async with session.request(
            method, url, headers=self.config.headers, json=json, timeout=self.config.timeout
        ) as response:
            try:
                data = await response.json()
                return data
            except (
                HTTPException,
                FaunaException,
                ValueError,
                KeyError,
                TypeError,
                Exception,
            ) as exc:  # pylint:disable=broad-exception-caught, unused-variable
                self.config.logger.error(exc)
                raise self.config.exception_class from exc
                
    async def text(
        self,
        url: str,
        method: Method = "GET",
        json: MaybeJson = None,
    ):
        session = self.__load__()
        async with session.request(
            method, url, headers=self.config.headers, json=json, timeout=self.config.timeout
        ) as response:
            try:
                data = await response.text()
                return data
            except (
                HTTPException,
                FaunaException,
                ValueError,
                KeyError,
                TypeError,
                Exception,
            ) as exc:  # pylint:disable=broad-exception-caught, unused-variable
                self.config.logger.error(exc)
                raise self.config.exception_class from exc

    async def stream(
        self,
        url: str,
        method: Method = "GET",
        json: MaybeJson = None,
    ):
        session = self.__load__()
        async with session.request(
            method, url, headers=self.config.headers, json=json, timeout=30
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
                ) as exc:
                    self.config.logger.error(exc)
                    yield str(exc)
                    raise self.config.exception_class from exc
                    
    
    def update_headers(self, headers: Dict[str,str]):
        """
        Update the headers used by this API client.

        Returns:
            self: Allows method chaining.
        """
        self.config.headers = headers
        return self