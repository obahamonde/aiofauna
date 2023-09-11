import asyncio
import io
from asyncio import BaseTransport
from typing import Any, Awaitable, Callable, MutableMapping, Tuple

from .server import APIServer
from aiohttp import web
from aiohttp.http_parser import RawRequestMessage
from aiohttp.payload import StringPayload
from multidict import CIMultiDict, CIMultiDictProxy
from yarl import URL

Scope = MutableMapping[str, Any]
Message = MutableMapping[str, Any]
Receive = Callable[[], Awaitable[Message]]
Send = Callable[[Message], Awaitable[None]]

ASGIApp = Callable[[Scope, Receive, Send], Awaitable[None]]

class ASGITransport(BaseTransport):
	"""ASGI Lambda Transport."""
	scheme: str

	@classmethod
	def from_scope(cls, scope: Scope):
		"""Create a transport from a scope."""
		cls.scheme = scope["scheme"]
		return cls
		
	def get_extra_info(self, name: str, default: Any = None) -> Any:
		"""Get extra information."""
		return None

class ASGIProtocol(web.RequestHandler):
	"""ASGI Lambda Protocol."""
	http_version: str

	@classmethod
	def from_scope(cls, scope: Scope):
		"""Create a protocol from a scope."""
		cls.http_version = scope["http_version"]
		cls.transport = ASGITransport.from_scope(scope)() # type: ignore
		return cls

		
class ASGIServer(APIServer):
	"""
	An ASGI-compatible API.

	Currently only supports HTTP and is compatible with ASGI 2.0.

	Tested with:
	`uvicorn`
	`daphne`[TODO]

	"""

	async def asgi(self, scope: Scope, _:Receive, send: Send) -> None:
		"""ASGI Wrapper."""

		if scope["type"] != "http":
			raise RuntimeError("Only HTTP is supported")

		raw_headers: Tuple[Tuple[bytes, bytes], ...] = scope["headers"]
		headers:CIMultiDict[str] = CIMultiDict()
		for k, v in raw_headers:
			headers[k.decode().lower()] = v.decode()

		message = RawRequestMessage(
			method=scope["method"],
			path=scope["path"],
			version=scope["http_version"],
			headers=CIMultiDictProxy(headers),
			raw_headers=raw_headers,
			should_close=True,
			compression=None,
			upgrade=False,
			chunked=True,
			url=URL(scope["path"]),
		)

		

		
		request = web.Request(
			message=message,
			payload=io.BytesIO(),
			protocol=ASGIProtocol.from_scope(scope),
			payload_writer=None,
			task=None,
			loop=asyncio.get_running_loop(),
		)

		response = await self._handle(request)

		body = response._body
		if isinstance(body, StringPayload):
			body = body._value
		if isinstance(body, str):
			body = body.encode()

		await send(
			{
				"type": "http.response.start",
				"status": response.status,
				"headers": [
					(k.encode(), v.encode()) for k, v in response.headers.items()
				],
			}
		)

		await send({"type": "http.response.body", "body": body, "more_body": False})

	async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
		"""ASGI callable."""
		return await self.asgi(scope, receive, send)
	
	