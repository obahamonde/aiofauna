"""REST API Module with automatic OpenAPI generation."""
import asyncio
import os
import threading
import time
from functools import wraps
from inspect import signature
from typing import Awaitable, Callable

from aiohttp.typedefs import Handler
from aiohttp.web import (Application, AppRunner, FileResponse, Request,
                         Response, StreamResponse, TCPSite, json_response,
                         run_app)
from aiohttp.web_exceptions import HTTPException
from aiohttp.web_middlewares import middleware
from aiohttp.web_ws import WebSocketResponse
from aiohttp_sse import EventSourceResponse, sse_response

from .client import ApiClient, FaunaClient
from .docs import extract, html, load, transform
from .helpers import do_response
from .json import jsonable_encoder
from .logging import setup_logging
from .odm import FaunaModel

Middleware = Callable[[Request, Handler], Awaitable[StreamResponse]]


class AioFauna(Application):
    """Aiohttp Application with automatic OpenAPI generation."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, logger=setup_logging(self.__class__.__name__), **kwargs)
        self.openapi = {
            "openapi": "3.0.0",
            "info": {"title": "AioFauna", "version": "1.0.0"},
            "paths": {},
            "components": {"schemas": {}},
            "description": "AioFauna API",
        }
        self._route_open_api_params = {}

        @self.get("/openapi.json")
        async def openapi():
            response = jsonable_encoder(self.openapi)
            return response

        @self.get("/docs")
        async def docs():
            return Response(text=html, content_type="text/html")
        
        @self.on_event("startup")
        async def startup(_):
            await FaunaModel.create_all()
            
        @self.on_event("shutdown")
        async def shutdown(_):
            await ApiClient.cleanup()
            await FaunaModel.cleanup()
    def document(self, path: str, method: str):
        """

        Decorator to document a function.

        """

        def decorator(func):
            sig = signature(func)
            params = sig.parameters
            open_api_params = extract(params.copy(), path)
            self._route_open_api_params[(path, method)] = open_api_params
            transform(self.openapi, path, method, func, open_api_params)

            async def wrapper(*args, **kwargs):
                request: Request = args[0]
                args = args[1:]
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
                if asyncio.iscoroutinefunction(func):
                    response = await func(*args, **kwargs, **definitive_args)
                else:
                    response = func(*args, **kwargs, **definitive_args)
                return do_response(response)

            func.injectable = True
            wrapper._handler = func
            return wrapper

        return decorator

    def get(self, path: str, **kwargs):
        """GET decorator"""

        def decorator(func):
            self.router.add_get(path, self.document(path, "GET")(func), **kwargs)
            return func

        return decorator

    def post(self, path: str, **kwargs):
        """POST decorator"""

        def decorator(func):
            self.router.add_post(path, self.document(path, "POST")(func), **kwargs)
            return func

        return decorator

    def put(self, path: str, **kwargs):
        """PUT decorator"""

        def decorator(func):
            self.router.add_put(path, self.document(path, "PUT")(func), **kwargs)
            return func

        return decorator

    def delete(self, path: str, **kwargs):
        """DELETE decorator"""

        def decorator(func):
            self.router.add_delete(path, self.document(path, "DELETE")(func), **kwargs)
            return func

        return decorator

    def patch(self, path: str, **kwargs):
        """PATCH decorator"""

        def decorator(func):
            self.router.add_patch(path, self.document(path, "PATCH")(func), **kwargs)
            return func

        return decorator

    def head(self, path: str, **kwargs):
        """HEAD decorator"""

        def decorator(func):
            self.router.add_head(path, self.document(path, "HEAD")(func), **kwargs)
            return func

        return decorator

    def options(self, path: str, **kwargs):
        """OPTIONS decorator"""

        def decorator(func):
            self.router.add_options(
                path, self.document(path, "OPTIONS")(func), **kwargs
            )
            return func

        return decorator

    def on_event(self, event: str):
        """On event handler"""

        def decorator(func):
            if event not in ("startup", "shutdown"):
                raise ValueError("Event must be startup or shutdown")
            elif event == "startup":
                self.on_startup.append(func)
            else:
                self.on_shutdown.append(func)
            return func

        return decorator

    def sse(self, path: str) -> Callable:  # pylint: disable=invalid-name
        """Server-Sent Events decorator"""

        def decorator(func: Callable) -> Callable:
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

            self.router.add_get(path, wrapper)
            return wrapper

        return decorator

    def websocket(self, path: str) -> Callable:  # pylint: disable=invalid-name
        """Websocket decorator"""

        def decorator(func: Callable) -> Callable:
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

    def static(self):
        """Static folder creation and serving"""
        try:
            os.makedirs("static", exist_ok=True)
        except OSError:
            pass
        self.router.add_static("/", "static")

        @self.get("/")
        def index():
            return FileResponse("static/index.html")

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



    def run(self, host:str="0.0.0.0", port:int=8080):
        """Run the server"""
        self.should_restart = False
        self.logger.info("Starting server at http://%s:%s", host, port) 
        self.logger.info("Press Ctrl+C to stop the server")
        self.runner = AppRunner(self)

        # Monitor for file changes in a separate thread
        self.file_change_monitor_thread = threading.Thread(target=self.monitor_files, daemon=True)
        self.file_change_monitor_thread.start()

        while True:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.runner.setup())        
            site = TCPSite(self.runner, host, port)     
            loop.run_until_complete(site.start())
            self.logger.info("Server started")
            self.logger.info("Swagger UI available at http://%s:%s/docs", host, port)
            self.logger.info("OpenAPI JSON available at http://%s:%s/openapi.json", host, port)
            
            try:
                loop.run_forever()
            except KeyboardInterrupt:
                self.logger.info("Stopping server")
                loop.run_until_complete(self.runner.cleanup())
                loop.run_until_complete(self.shutdown())
                loop.run_until_complete(self.cleanup())
                loop.close()
                self.logger.info("Server stopped")
                break
            finally:
                if self.should_restart:
                    self.logger.info("File change detected. Restarting server...")
                    loop.run_until_complete(self.runner.cleanup())
                    loop.run_until_complete(self.shutdown())
                    loop.run_until_complete(self.cleanup())
                    loop.close()
                    self.should_restart = False

    def monitor_files(self):
        """Monitor for changes in Python files and restart the server if a change is detected"""
        paths_to_track = [os.getcwd()]
        file_modification_times = self.track_files(os.getcwd())
        while True:
            for path in paths_to_track:
                for file_path, last_modified in self.track_files(path).items():
                    if file_path not in file_modification_times:
                        file_modification_times[file_path] = last_modified
                    elif file_modification_times[file_path] != last_modified:
                        self.should_restart = True
                        return
            
    @staticmethod
    def track_files(path):
        """Get the modification times for all Python files in the specified path"""
        file_modification_times = {}
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if filename.endswith(".py"):
                    file_path = os.path.join(dirpath, filename)
                    file_modification_times[file_path] = os.path.getmtime(file_path)
        return file_modification_times

    def restart(self):
        """Restart the server"""
        self.logger.info("Restarting server")
        loop = asyncio.get_event_loop()
        loop.call_soon_threadsafe(loop.stop)