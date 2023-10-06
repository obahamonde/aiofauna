"""
This module provides utilities for creating HTTP clients using aiohttp and Pydantic.

.. moduleauthor:: Your Name <your.email@example.com>
"""

from functools import wraps
from typing import (
    Any,
    AsyncGenerator,
    Awaitable,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Type,
    TypeVar,
    Union,
)

from aiohttp import ClientSession, ClientTimeout, TCPConnector, UnixConnector
from aiohttp.web import Response
from pydantic import Field, root_validator  # pylint: disable=no-name-in-module
from pydantic.main import ModelMetaclass  # pylint: disable=no-name-in-module
from typing_extensions import ParamSpec

from ..data.document import Document

Method = Literal["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]
Json = Union[Dict[str, Any], List[Dict[str, Any]]]
MaybeJson = Optional[Json]


T = TypeVar("T")
P = ParamSpec("P")
M = TypeVar("M", bound=ModelMetaclass)


class SingletonModelMeta(ModelMetaclass):
    """
    Singleton metaclass for Pydantic models.
    ----------------------------------------

    Monkey patches the Pydantic metaclass to ensure that only one instance of a model is created.
    """

    _instances = {}

    def __call__(
        cls, *args: Any, **kwargs: Any
    ):  # pylint: disable=E0213 # type: ignore
        if cls not in cls._instances:  # type: ignore
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance  # type: ignore
        return cls._instances[cls]  # type: ignore


def injectable(
    factory: Callable[[], ClientSession]
) -> Callable[[Callable[P, Any]], Callable[P, Awaitable[Response]]]:
    """
    Injectable
    ----------

    A decorator that injects a `ClientSession` instance into the decorated handler.

    :param factory: A callable that returns a ClientSession instance.
    :type factory: Callable[[], ClientSession]
    :returns: A decorator that injects a `ClientSession` instance into the decorated handler.
    """

    def decorator(func: Callable[P, Any]) -> Callable[P, Awaitable[Response]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
            for k, v in kwargs.items():
                if isinstance(v, Client):
                    kwargs[k] = factory()
            return await func(*args, **kwargs)

        return wrapper

    return decorator


class Client(Document, metaclass=SingletonModelMeta):  # pylint: disable=E1139
    """
    Client
    ------

    Base Client that is subclassed to create a client for a specific API.

    Features singleton pattern to ensure that only one instance of a client is created allowing session reuse for the same instance configuration.

    :param base_url: The base URL for the API.
    :type base_url: str
    :param headers: The headers to use for the API.
    :type headers: dict[str, str]
    :param limit: The maximum number of connections to allow.
    :type limit: int
    :param timeout: The timeout for the API.
    :type timeout: int
    :param connector_type: The type of connector to use.
    :type connector_type: Literal["tcp", "unix"]

    .. note:: The `connector` and `session` fields are not included in the schema.
    """

    base_url: str = Field(...)
    headers: dict[str, str] = Field(default={"Content-Type": "application/json"})
    limit: int = Field(default=1000, ge=1, le=10000)
    timeout: int = Field(default=10, ge=1, le=100)
    connector_type: Literal["tcp", "unix"] = Field(default="tcp")

    @staticmethod
    def schema_extra(schema: dict[str, Any], _: Type["Client"]) -> None:  # type: ignore
        """
        Removes the `connector` and `session` fields from the schema.
        """
        schema["properties"].pop("connector")
        schema["properties"].pop("session")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.base_url})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.base_url})"

    def dict(self, *args: Any, **kwargs: Any):
        # Call the superclass's dict method
        """
        Removes the `headers` field from the dictionary representation.
        """
        dct = super().dict(*args, **kwargs)
        # Remove the headers field
        dct.pop("headers", None)
        return dct

    @classmethod
    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)  # type: ignore

    @root_validator(pre=False, skip_on_failure=True)
    @classmethod
    def validate_args(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates the arguments passed to the constructor.
        """

        if values["connector_type"] == "tcp":
            values["connector"] = TCPConnector(limit=values["limit"])
        elif values["connector_type"] == "unix":
            values["connector"] = UnixConnector(
                path=values["base_url"], limit=values["limit"]
            )
        values["timeout"] = ClientTimeout(total=values["timeout"])
        values["session"] = ClientSession(
            base_url=values["base_url"],
            headers=values["headers"],
            connector=values["connector"],
            timeout=values["timeout"],
        )
        return values

    def __call__(self) -> ClientSession:
        """
        Returns the `ClientSession` instance.
        """
        return getattr(self, "session")

    async def request(
        self, method: Method, path: str, json: MaybeJson = None, **kwargs: Any
    ):
        """
        Makes an HTTP request.

        :param method: The HTTP method to use.
        :type method: str
        :param path: The path to request.
        :type path: str
        :param kwargs: Additional keyword arguments to pass to the request.
        :type kwargs: Any
        :return: The response data.
        :rtype: Any
        """
        response = await self().request(method, path, json=json, **kwargs)
        if "json" in response.content_type:
            return await response.json()
        if "text" in response.content_type:
            return await response.text()
        else:
            return await response.read()

    async def get(self, path: str, **kwargs: Any) -> Any:
        """
        Makes a GET request.

        :param path: The path to request.
        :type path: str
        :param kwargs: Additional keyword arguments to pass to the request.
        :type kwargs: Any
        :return: The response data.
        :rtype: Any
        """
        return await self.request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs: Any) -> Any:
        """
        Makes a POST request.

        :param path: The path to request.
        :type path: str
        :param kwargs: Additional keyword arguments to pass to the request.
        :type kwargs: Any
        :return: The response data.
        :rtype: Any
        """
        return await self.request("POST", path, **kwargs)

    async def put(self, path: str, **kwargs: Any) -> Any:
        """
        Makes a PUT request.

        :param path: The path to request.
        :type path: str
        :param kwargs: Additional keyword arguments to pass to the request.
        :type kwargs: Any
        :return: The response data.
        :rtype: Any
        """
        return await self.request("PUT", path, **kwargs)

    async def patch(self, path: str, **kwargs: Any) -> Any:
        """
        Makes a PATCH request.

        :param path: The path to request.
        :type path: str
        :param kwargs: Additional keyword arguments to pass to the request.
        :type kwargs: Any
        :return: The response data.
        :rtype: Any
        """
        return await self.request("PATCH", path, **kwargs)

    async def delete(self, path: str, **kwargs: Any) -> Any:
        """
        Makes a DELETE request.

        :param path: The path to request.
        :type path: str
        :param kwargs: Additional keyword arguments to pass to the request.
        :type kwargs: Any
        :return: The response data.
        :rtype: Any
        """
        return await self.request("DELETE", path, **kwargs)

    async def head(self, path: str, **kwargs: Any) -> Any:
        """
        Makes a HEAD request.

        :param path: The path to request.
        :type path: str
        :param kwargs: Additional keyword arguments to pass to the request.
        :type kwargs: Any
        :return: The response data.
        :rtype: Any
        """
        return await self.request("HEAD", path, **kwargs)

    async def options(self, path: str, **kwargs: Any) -> Any:
        """
        Makes an OPTIONS request.

        :param path: The path to request.
        :type path: str
        :param kwargs: Additional keyword arguments to pass to the request.
        :type kwargs: Any
        :return: The response data.
        :rtype: Any
        """
        return await self.request("OPTIONS", path, **kwargs)

    async def stream(
        self, path: str, method: str = "GET", **kwargs: Any
    ) -> AsyncGenerator[bytes, None]:
        """
        Streams a response.

        :param path: The path to request.
        :type path: str
        :param method: The HTTP method to use.
        :type method: str
        :param kwargs: Additional keyword arguments to pass to the request.
        :type kwargs: Any
        :return: The response data.
        :rtype: AsyncGenerator[bytes, None]
        """
        async with self().request(method, path, **kwargs) as response:
            async for chunk in response.content.iter_any():
                yield chunk

    async def text(self, path: str, method: str = "GET", **kwargs: Any) -> str:
        """
        Returns the response as text.

        :param path: The path to request.
        :type path: str
        :param method: The HTTP method to use.
        :type method: str
        :param kwargs: Additional keyword arguments to pass to the request.
        :type kwargs: Any
        :return: The response data.
        :rtype: str
        """
        async with self().request(method, path, **kwargs) as response:
            return await response.text()

    async def blob(self, path: str, method: str = "GET", **kwargs: Any) -> bytes:
        """
        Returns the response as bytes.

        :param path: The path to request.
        :type path: str
        :param method: The HTTP method to use.
        :type method: str
        :param kwargs: Additional keyword arguments to pass to the request.
        :type kwargs: Any
        :return: The response data.
        :rtype: bytes
        """
        async with self().request(method, path, **kwargs) as response:
            return await response.read()
