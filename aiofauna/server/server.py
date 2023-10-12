"""REST API Module with automatic OpenAPI generation."""
import asyncio
import os
from functools import wraps
from inspect import signature
from typing import (Any, Awaitable, Callable, Coroutine, List, Literal,
                    Optional, TypeVar, cast)

from aiohttp.typedefs import Handler
from aiohttp.web import (Application, HTTPFound, Request, Response,
                         StreamResponse)
from aiohttp.web_middlewares import middleware
from aiohttp.web_ws import WebSocketResponse
from aiohttp_sse import EventSourceResponse, sse_response
from typing_extensions import ParamSpec

from ..data.document import Document
from ..data.json import jsonable_encoder
from ..data.odm import FaunaModel
from ..helpers import do_response
from ..utils import setup_logging
from .docs import extract, html_string, load, transform
from .router import APIRouter

P = ParamSpec("P")
_T = TypeVar("_T")

Middleware = Callable[[Request, Handler], Awaitable[StreamResponse]]


class APIServer(Application):
	"""
	AioFauna APIServer class for handling API operations.

	:param title: The title of the API.
	:type title: str
	:param servers: List of server URLs.
	:type servers: list[str]
	:param description: API description.
	:type description: str
	:param version: API version.
	:type version: str
	:param openapi_url: URL for OpenAPI documentation.
	:type openapi_url: str
	"""

	def __init__(
		self,
		*args: Any,
		title: str = "AioFauna",
		servers: Optional[List[str]] = None,
		version: str = "0.0.1",
		openapi_url: str = "/openapi.json",
		**kwargs: Any,
	):
		super().__init__(*args, logger=setup_logging(self.__class__.__name__), **kwargs)
		schemas = FaunaModel.Metadata.subclasses + Document.Metadata.subclasses
		self.openapi = {
			"openapi": "3.1.0",
			"info": {"title": title, "version": version},
			"paths": {},
			"servers": [{"url": url} for url in servers or []],
			"components": {
				"schemas": {schema.__name__: schema.schema() for schema in schemas}
			},
		}
		self._route_open_api_params = {}
		self.openapi_url: str = openapi_url

		@self.get("/openapi.json")
		async def openapi():
			response = jsonable_encoder(self.openapi)
			return response

		@self.get("/docs")
		async def docs():
			return Response(
				text=html_string(self.openapi_url), content_type="text/html"
			)

	def document(
		self, path: str, method: str
	) -> Callable[
		[Callable[P, Coroutine[Any, Any, _T]]], Callable[P, Coroutine[Any, Any, _T]]
	]:
		"""

		Decorator to generate OpenAPI documentation for an endpoint handler.

		:param path: The URL path of the endpoint.
		:type path: str
		:param method: The HTTP method of the endpoint.
		:type method: str
		:return: Decorated function for handling the endpoint.
		:rtype: Callable

		"""

		def decorator(
			func: Callable[P, Coroutine[Any, Any, _T]]
		) -> Callable[P, Coroutine[Any, Any, _T]]:
			sig = signature(func)
			params = sig.parameters
			open_api_params = extract(params.copy(), path)
			self._route_open_api_params[(path, method)] = open_api_params
			transform(self.openapi, path, method, func, open_api_params)

			async def wrapper(*args: P.args, **kwargs: P.kwargs) -> StreamResponse:
				request = cast(Request, args[0])
				new_args = args[1:]
				args_to_apply = await load(request, params.copy())
				definitive_args = {}
				for name, param in params.items():
					if name in args_to_apply:
						definitive_args[name] = args_to_apply[name]
					elif param.default is not param.empty:
						definitive_args[name] = param.default
					else:
						raise ValueError(
							f"Missing parameter {name} for {func.__name__}"
						)
				response = await func(*new_args, **definitive_args, **kwargs)  # type: ignore
				return do_response(response)

			wrapper._handler = func
			wrapper.__name__ = func.__name__
			return cast(Callable[P, Coroutine[Any, Any, _T]], wrapper)

		return decorator

	def get(
		self, path: str, **kwargs: Any
	) -> Callable[[Callable[P, Awaitable[_T]]], Callable[P, Awaitable[_T]]]:
		"""
		Decorator for handling GET requests.

		:param path: The API path for the GET request.
		:type path: str
		:return: Decorated function for handling the GET request.
		:rtype: Callable
		"""

		def decorator(
			func: Callable[P, Awaitable[StreamResponse]]
		) -> Callable[P, Awaitable[StreamResponse]]:
			self.router.add_get(path, self.document(path, "GET")(func), **kwargs)
			return func

		return decorator

	def post(
		self, path: str, **kwargs: Any
	) -> Callable[[Callable[P, Awaitable[_T]]], Callable[P, Awaitable[_T]]]:
		"""
		Decorator for handling POST requests.

		:param path: The API path for the POST request.
		:type path: str
		:return: Decorated function for handling the POST request.
		:rtype: Callable
		"""

		def decorator(
			func: Callable[P, Awaitable[StreamResponse]]
		) -> Callable[P, Awaitable[StreamResponse]]:
			self.router.add_post(path, self.document(path, "POST")(func), **kwargs)
			return func

		return decorator

	def put(
		self, path: str, **kwargs: Any
	) -> Callable[[Callable[P, Awaitable[_T]]], Callable[P, Awaitable[_T]]]:
		"""
		Decorator for handling PUT requests.

		:param path: The API path for the PUT request.
		:type path: str
		:return: Decorated function for handling the PUT request.
		:rtype: Callable

		"""

		def decorator(
			func: Callable[P, Awaitable[StreamResponse]]
		) -> Callable[P, Awaitable[StreamResponse]]:
			self.router.add_put(path, self.document(path, "PUT")(func), **kwargs)
			return func

		return decorator

	def delete(
		self, path: str, **kwargs: Any
	) -> Callable[[Callable[P, Awaitable[_T]]], Callable[P, Awaitable[_T]]]:
		"""
		Decorator for handling DELETE requests.

		:param path: The API path for the DELETE request.
		:type path: str
		:return: Decorated function for handling the DELETE request.
		:rtype: Callable

		"""

		def decorator(
			func: Callable[P, Awaitable[StreamResponse]]
		) -> Callable[P, Awaitable[StreamResponse]]:
			self.router.add_delete(path, self.document(path, "DELETE")(func), **kwargs)
			return func

		return decorator

	def patch(
		self, path: str, **kwargs: Any
	) -> Callable[[Callable[P, Awaitable[_T]]], Callable[P, Awaitable[_T]]]:
		"""

		Decorator for handling PATCH requests.

		:param path: The API path for the PATCH request.
		:type path: str
		:return: Decorated function for handling the PATCH request.
		:rtype: Callable

		"""

		def decorator(
			func: Callable[P, Awaitable[StreamResponse]]
		) -> Callable[P, Awaitable[StreamResponse]]:
			self.router.add_patch(path, self.document(path, "PATCH")(func), **kwargs)
			return func

		return decorator

	def head(
		self, path: str, **kwargs: Any
	) -> Callable[[Callable[P, Awaitable[_T]]], Callable[P, Awaitable[_T]]]:
		"""

		Decorator for handling HEAD requests.

		:param path: The API path for the HEAD request.
		:type path: str
		:return: Decorated function for handling the HEAD request.
		:rtype: Callable

		"""

		def decorator(
			func: Callable[P, Awaitable[StreamResponse]]
		) -> Callable[P, Awaitable[StreamResponse]]:
			self.router.add_head(path, self.document(path, "HEAD")(func), **kwargs)
			return func

		return decorator

	def options(
		self, path: str, **kwargs: Any
	) -> Callable[[Callable[P, Awaitable[_T]]], Callable[P, Awaitable[_T]]]:
		"""

		Decorator for handling OPTIONS requests.

		:param path: The API path for the OPTIONS request.
		:type path: str
		:return: Decorated function for handling the OPTIONS request.
		:rtype: Callable

		"""

		def decorator(
			func: Callable[P, Awaitable[StreamResponse]]
		) -> Callable[P, Awaitable[StreamResponse]]:
			self.router.add_options(
				path, self.document(path, "OPTIONS")(func), **kwargs
			)
			return func

		return decorator

	def on_event(
		self, event: Literal["startup", "shutdown"]
	) -> Callable[
		[Callable[[Application], Awaitable[None]]],
		Callable[[Application], Awaitable[None]],
	]:
		"""

		Decorator for handling startup and shutdown lifecycle events.

		:param event: The event to handle (startup or shutdown).

		"""

		def decorator(
			func: Callable[[Application], Awaitable[None]]
		) -> Callable[[Application], Awaitable[None]]:
			if event not in ("startup", "shutdown"):
				raise ValueError("Event must be startup or shutdown")
			elif event == "startup":
				self.on_startup.append(func)
			else:
				self.on_shutdown.append(func)
			return func

		return decorator

	def sse(
		self, path: str
	) -> Callable[
		[Callable[P, Awaitable[EventSourceResponse]]],
		Callable[P, Awaitable[EventSourceResponse]],
	]:
		"""

		Server-Sent Events decorator.

		:param path: The API path for the SSE request.
		:type path: str
		:return: Decorated function for handling the SSE request.

		This decorator will handle SSE connections and pass the response object to the decorated function, be sure to include a parameter with the type annotation `EventSourceResponse` in your function signature.
		You can use the `send` method of the response object to send events to the client.

		Example:

		.. code-block:: python

		import asyncio
		from aiofauna import FaunaClient, APIServer, EventSourceResponse, to_json,q

		app = APIServer()
		fauna = FaunaClient()

		@app.sse("/stream")
		async def stream(sse: EventSourceResponse):
				while True:
						now = await fauna.query(q.now())
						await sse.send(to_json(now["@ts"]))
						await asyncio.sleep(1)

		"""

		def decorator(
			func: Callable[P, Awaitable[EventSourceResponse]]
		) -> Callable[P, Awaitable[EventSourceResponse]]:
			@wraps(func)
			async def wrapper(request: Request) -> EventSourceResponse:
				async with sse_response(request) as resp:
					args_to_apply = await load(
						request, signature(func).parameters.copy()
					)
					definitive_args = {}
					for name, param in signature(func).parameters.items():
						if param.annotation == EventSourceResponse:
							definitive_args[name] = resp
						elif name in args_to_apply:
							definitive_args[name] = args_to_apply[name]
							args_to_apply.pop(name)
						elif param.default is not param.empty:
							definitive_args[name] = param.default
						else:
							raise ValueError(
								f"Missing parameter {name} for {func.__name__}"
							)
					await func(**definitive_args)
					return resp

			self.router.add_get(path, self.document(path, "OPTIONS")(wrapper))
			return wrapper

		return decorator

	def websocket(
		self, path: str
	) -> Callable[
		[Callable[P, Awaitable[WebSocketResponse]]],
		Callable[P, Awaitable[WebSocketResponse]],
	]:
		"""

		Websocket decorator.

		:param path: The API path for the websocket request.
		:type path: str
		:return: Decorated function for handling the websocket request.

		This decorator will handle websocket connections and pass the websocket object to the decorated function, be sure to include a parameter with the type annotation `WebSocketResponse` in your function signature and also setup proper error handling, since `PING` and `PONG` messages are handled automatically by the server and will result on a `MessageTypeError` if not handled.

		"""

		def decorator(
			func: Callable[P, Awaitable[WebSocketResponse]]
		) -> Callable[P, Awaitable[WebSocketResponse]]:
			@wraps(func)
			async def wrapper(request: Request):
				args_to_apply = await load(request, signature(func).parameters.copy())
				ws = WebSocketResponse()
				await ws.prepare(request)
				definitive_args = {}
				for name, param in signature(func).parameters.items():
					if param.annotation == WebSocketResponse:
						definitive_args[name] = ws
					elif name in args_to_apply:
						definitive_args[name] = args_to_apply[name]
						args_to_apply.pop(name)
					elif param.default is not param.empty:
						definitive_args[name] = param.default
					else:
						raise ValueError(
							f"Missing parameter {name} for {func.__name__}"
						)
				await func(**definitive_args)
				return ws

			self.router.add_get(path, wrapper)
			return wrapper

		return decorator

	def static(self,path:str="",dir:str="static") -> "APIServer":
		"""

		Static files decorator.

		This decorator will serve static files from the `static` directory.
		It will also serve the `index.html` file from the `static` directory when the root path is requested.
		Useful for serving a frontend single-page application.

		:return: The server instance.

		"""

		@self.get(f"/{path}")
		async def index(request:Request):
			base_url = request.url.path
			return HTTPFound(location=f"{base_url}/{path}/index.html")

		try:
			os.makedirs(dir, exist_ok=True)
		except OSError:
			pass
		self.router.add_static(f"/{path}", dir)

		return self

	def middleware(self, func: Middleware) -> Middleware:
		@wraps(func)
		@middleware
		async def wrapper(request: Request, handler: Handler) -> Response:
			response = await func(request, handler)
			if isinstance(response, Response):
				return response
			return do_response(response)

		self.middlewares.append(wrapper)
		return wrapper

	def use(self, router: APIRouter, prefix: str = "") -> "APIServer":
		"""Chainable method to add a router to the server"""
		for route in router.routes:
			path = prefix + route.path
			self.router.add_route(
				route.method,
				prefix + router.prefix + path,
				route.handler,
				**route.kwargs,
			)

		for path, details in router.openapi["paths"].items():
			path = prefix + path
			self.openapi["paths"][path] = details

		self.openapi["components"]["schemas"].update(
			router.openapi["components"]["schemas"]
		)
		return self
