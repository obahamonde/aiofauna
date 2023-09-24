"""
This module provides utilities for creating HTTP clients using aiohttp and Pydantic.

.. moduleauthor:: Your Name <your.email@example.com>
"""
import os
from functools import wraps
from threading import Lock
from typing import (Any, AsyncGenerator, Awaitable, Callable, Dict, Literal,
                    Type, TypeVar)

from aiohttp import ClientSession, ClientTimeout, TCPConnector, UnixConnector
from aiohttp.web import Response
from pydantic import Field, root_validator  # pylint: disable=no-name-in-module
from typing_extensions import ParamSpec

from .typedefs import Document

T = TypeVar("T")
P = ParamSpec("P")

def injectable(factory: Callable[[], ClientSession]) -> Callable[[Callable[P, Any]], Callable[P, Awaitable[Response]]]:
	"""
	A decorator that injects a ClientSession instance into the decorated function.

	:param factory: A callable that returns a ClientSession instance.
	:type factory: Callable[[], ClientSession]
	:returns: A decorator
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

def singleton(cls: Type[T]) -> None:  # type: ignore
	cls._instace = None
	cls._lock = Lock()

	@wraps(cls)
	def wrapper(*args: Any, **kwargs: Any) -> T:
		with cls._lock:
			if cls._instace is None:
				cls._instace = cls(*args, **kwargs)
			return cls._instace
	return wrapper


class Client(Document):
	"""
	Base Client that must be subclassed to create a client for a specific API.

	:ivar base_url: The base URL for the API.
	:vartype base_url: str
	:ivar headers: HTTP headers to include in requests.
	:vartype headers: dict[str, str]
	:ivar limit: The maximum number of connections.
	:vartype limit: int
	:ivar timeout: The timeout for requests.
	:vartype timeout: int
	:ivar connector_type: The type of connector to use ('tcp' or 'unix').
	:vartype connector_type: Literal["tcp", "unix"]
	"""
	base_url: str = Field(...)
	headers: dict[str, str] = Field(default={"Content-Type": "application/json"})
	limit: int = Field(default=1000, ge=1, le=10000)
	timeout: int = Field(default=10, ge=1, le=100)
	connector_type: Literal["tcp", "unix"] = Field(
		default="tcp"
	)

	@staticmethod
	def schema_extra(schema: dict[str, Any], model_class: Type["Client"]) -> None:  # type: ignore
		schema["properties"].pop("connector")
		schema["properties"].pop("session")

	def __repr__(self) -> str:
		return f"{self.__class__.__name__}({self.base_url})"
	
	def __str__(self) -> str:
		return f"{self.__class__.__name__}({self.base_url})"

	def dict(self, *args:Any, **kwargs:Any):
		# Call the superclass's dict method
		d = super().dict(*args, **kwargs)
		# Remove the headers field
		d.pop("headers", None)
		return d


	@classmethod
	def __init_subclass__(cls, **kwargs: Any) -> None:
		super().__init_subclass__(**kwargs) # type: ignore
		singleton(cls)


	@root_validator(pre=False, skip_on_failure=True)
	@classmethod
	def validate_args(cls, values: Dict[str, Any]) -> Dict[str, Any]:
		if values["connector_type"] == "tcp":
			values["connector"] = TCPConnector(limit=values["limit"])
		elif values["connector_type"] == "unix":
			values["connector"] = UnixConnector(path=values["base_url"], limit=values["limit"])
		values["timeout"] = ClientTimeout(total=values["timeout"])
		values["session"] = ClientSession(
			base_url=values["base_url"],
			headers=values["headers"],
			connector=values["connector"],
			timeout=values["timeout"],
		)
		return values
	
	def __call__(self) -> ClientSession:
		return getattr(self, "session")
	
	async def request(self, method: str, path: str, **kwargs: Any):
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
		response = await self().request(method, path, **kwargs)
		if "json" in response.content_type:
			return await response.json()
		elif "text" in response.content_type:
			return await response.text()
		else:
			return await response.read()
		
	async def get(self, path: str, **kwargs: Any) -> Any:
		return await self.request("GET", path, **kwargs)
	
	async def post(self, path: str, **kwargs: Any) -> Any:
		return await self.request("POST", path, **kwargs)
	
	async def put(self, path: str, **kwargs: Any) -> Any:
		return await self.request("PUT", path, **kwargs)
	
	async def patch(self, path: str, **kwargs: Any) -> Any:
		return await self.request("PATCH", path, **kwargs)
	
	async def delete(self, path: str, **kwargs: Any) -> Any:
		return await self.request("DELETE", path, **kwargs)
	
	async def stream(self, path: str, method: str = "GET", **kwargs: Any) -> AsyncGenerator[bytes, None]:
		async with self().request(method, path, **kwargs) as response:
			async for chunk in response.content.iter_any():
				yield chunk

	async def text(self, path: str, method: str = "GET", **kwargs: Any) -> str:
		async with self().request(method, path, **kwargs) as response:
			return await response.text()
		

FAUNA_SECRET = os.environ["FAUNA_SECRET"]
HEADERS = {
	"Authorization": f"Bearer {FAUNA_SECRET}",
	"Content-type": "application/json",
	"Accept": "application/json",
	"User-Agent": "aiofauna-framework",
}