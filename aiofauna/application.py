from __future__ import annotations
import asyncio
import jinja2
import asyncio
from aiofauna import asyncio
from aiohttp_sse import sse_response
from aiohttp.web import (
    Application,
    AppRunner,
    TCPSite,
    Request,
    Response,
    json_response,
)
from aiohttp import ClientSession
from typing import Callable, Coroutine
from functools import wraps
from inspect import signature
from aiofauna.odm import AsyncFaunaModel
from pydantic import BaseModel
from aiohttp.web_request import FileField
from aiohttp.web import (
    Application,
    AppRunner,
    TCPSite,
    Request,
    Response,
    json_response,
)


class App(Application):
    """
    
    This module defines the App class, which is a subclass of the aiohttp.web.Application class.
    The App class provides a simple way to create web applications with Jinja2 templates.

    Usage Example:
    
    ```python
    
    from aiohttp import web

    app = App()

    @app.template("index.html", func=example_function)
    async def index(request):
        return {"message": "Hello, World!"}

    @app.route("GET", "/hello")
    async def hello(request):
        return web.Response(text="Hello, World!")

    web.run_app(app)

     Args:
        *args: Positional arguments to be passed to the aiohttp.web.Application superclass.
        **kwargs: Keyword arguments to be passed to the aiohttp.web.Application superclass.
        
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))
        self.openapi = {
            "openapi": "3.0.0",
            "info": {"title": "Aiofauna", "version": "0.1.0"},
            "paths": {},
            "components": {},
        }

    def template(self, template_name: str, **kwargs):
        """
        Decorator to render a template and return an HTTP response.

        Args:
            template_name (str): The name of the template file.
            **kwargs: Keyword arguments representing context variables to be passed to the template.

        Returns:
            Callable: The decorator function.
        """

        def decorator(func):
            @wraps(func)
            async def wrapper(request: Request) -> Response:
                if asyncio.iscoroutinefunction(func):
                    data = await func(request)
                else:
                    data = func(request)
                template = self.jinja_env.get_template(template_name).render(**data)
                return Response(body=template.encode(), content_type="text/html")

            return wrapper

        return decorator

    def document(self, method: str, path: str, **kwargs):
        """
        Inspects the signature of the handler function and based on the parameters it constraints the Request object to the parameters shape.
        
        The parameters can be aither `Scalars` or `Models`.
        
        `Scalars`: `str`, `int`, `float`, `bool`
        
        `Models`: `BaseModel`, `AsyncFaunaModel`, `FileField`
        
        Those parameters are enforced and bound on the Request object. And added to the openapi documentation property.
        

        
        Args:
            method (str): The HTTP method for the route (e.g., "GET", "POST").
            path (str): The URL path for the route.
            **kwargs: Additional keyword arguments for the route.
            
        Returns:
        
            Callable: The decorator function.
            
        """

        def decorator(func):
            async def wrapper(request) -> Response:
                sig = signature(func)
                params = sig.parameters
                args_to_apply = {}
                open_api_params = {}
                for k, v in params.items():
                    if v.annotation in [str, int, float, bool]:
                        if k in request.query:
                            request[k] = v.annotation(request.query[k])
                            open_api_params[k] = {
                                "in": "query",
                                "name": k,
                                "schema": {"type": v.annotation.__name__},
                            }
                            args_to_apply[k] = request[k]
                        elif k in request.match_info:
                            request[k] = v.annotation(request.match_info[k])
                            open_api_params[k] = {
                                "in": "path",
                                "name": k,
                                "schema": {"type": v.annotation.__name__},
                            }
                            args_to_apply[k] = request[k]
                        elif k in request.headers:
                            request[k] = v.annotation(request.headers[k])
                            open_api_params[k] = {
                                "in": "header",
                                "name": k,
                                "schema": {"type": v.annotation.__name__},
                            }
                            args_to_apply[k] = request[k]
                        elif k in request.cookies:
                            request[k] = v.annotation(request.cookies[k])
                            open_api_params[k] = {
                                "in": "cookie",
                                "name": k,
                                "schema": {"type": v.annotation.__name__},
                            }
                            args_to_apply[k] = request[k]
                        else:
                            raise Exception(f"Missing parameter {k}")
                    elif v.annotation.__class__ in [BaseModel, AsyncFaunaModel]:
                        if request.method not in ["POST", "PUT", "PATCH"]:
                            raise Exception(
                                f"Method {request.method} not allowed for {k}"
                            )
                        if request.content_type == "application/json":
                            open_api_params[k] = {
                                "in": "body",
                                "name": k,
                                "schema": {
                                    "$ref": f"#/components/schemas/{v.annotation.__name__}"
                                },
                            }
                            request[k] = v.annotation(**await request.json())
                            args_to_apply[k] = request[k]
                        elif request.content_type == "multipart/form-data":
                            open_api_params[k] = {
                                "in": "body",
                                "name": k,
                                "schema": {
                                    "$ref": f"#/components/schemas/{v.annotation.__name__}"
                                },
                            }
                            request[k] = v.annotation(**await request.post())
                            args_to_apply[k] = request[k]
                        else:
                            raise Exception(
                                f"Content type {request.content_type} not supported"
                            )
                    elif v.annotation.__class__ == FileField:
                        if request.method not in ["POST", "PUT", "PATCH"]:
                            raise Exception(
                                f"Method {request.method} not allowed for {k}"
                            )
                        if request.content_type == "multipart/form-data":
                            open_api_params[k] = {
                                "in": "body",
                                "name": k,
                                "schema": {"type": "string", "format": "binary"},
                            }
                            request[k] = await request.post()
                            args_to_apply[k] = request[k]
                        else:
                            raise Exception(
                                f"Content type {request.content_type} not supported"
                            )
                    else:
                        raise Exception(f"Type {v.annotation} not supported")
                    self.openapi["paths"][path] = {
                        method.lower(): {
                            "summary": func.__name__,
                            "description": func.__doc__,
                            "parameters": list(open_api_params.values()),
                            "responses": {"200": {"description": "OK"}},
                        }
                    }
                if asyncio.iscoroutinefunction(func):
                    return await func(request, **args_to_apply)
                return func(request, **args_to_apply)

            return wrapper

        return decorator

    async def listen(self, host: bool = False, port: int = 8000, **kwargs):

        """
        
        Starts Listening for requests.
        
        Args:
        
            host (str): The host to listen on.
            
            port (int): The port to listen on.
            
            **kwargs: Additional keyword arguments for the server.
            
        """
        if not host:
            _host = "localhost"
        _host = "0.0.0.0"
        runner = AppRunner(self, **kwargs)
        await runner.setup()
        site = TCPSite(runner, _host, port)
        await site.start()
        while True:
            await asyncio.sleep(1)

    def get(self, path: str, **kwargs):
        """
        Decorator to add a GET route.

        Args:
            path (str): The URL path for the route.
            **kwargs: Additional keyword arguments for the route.

        Returns:
            Callable: The decorator function.
        """

        @wraps(self.document("GET", path, **kwargs))
        def decorator(func):
            self.router.add_route(
                "GET", path, self.document("GET", path, **kwargs)(func), **kwargs
            )
            return func

        return decorator

    def post(self, path: str, **kwargs):
        """
        Decorator to add a POST route.

        Args:
            path (str): The URL path for the route.
            **kwargs: Additional keyword arguments for the route.

        Returns:
            Callable: The decorator function.
        """

        @wraps(self.document("POST", path, **kwargs))
        def decorator(func):
            self.router.add_route(
                "POST", path, self.document("POST", path, **kwargs)(func), **kwargs
            )
            return func

        return decorator

    def put(self, path: str, **kwargs):
        """
        Decorator to add a PUT route.

        Args:
            path (str): The URL path for the route.
            **kwargs: Additional keyword arguments for the route.

        Returns:
            Callable: The decorator function.
        """

        @wraps(self.document("PUT", path, **kwargs))
        def decorator(func):
            self.router.add_route(
                "PUT", path, self.document("PUT", path, **kwargs)(func), **kwargs
            )
            return func

        return decorator

    def patch(self, path: str, **kwargs):
        """
        Decorator to add a PATCH route.

        Args:
            path (str): The URL path for the route.
            **kwargs: Additional keyword arguments for the route.

        Returns:
            Callable: The decorator function.
        """

        @wraps(self.document("PATCH", path, **kwargs))
        def decorator(func):
            self.router.add_route(
                "PATCH", path, self.document("PATCH", path, **kwargs)(func), **kwargs
            )
            return func

        return decorator

    def delete(self, path: str, **kwargs):
        """
        Decorator to add a DELETE route.

        Args:
            path (str): The URL path for the route.
            **kwargs: Additional keyword arguments for the route.

        Returns:
            Callable: The decorator function.
        """

        @wraps(self.document("DELETE", path, **kwargs))
        def decorator(func):
            self.router.add_route(
                "DELETE", path, self.document("DELETE", path, **kwargs)(func), **kwargs
            )
            return func

        return decorator

    def options(self, path: str, **kwargs):
        """
        Decorator to add a OPTIONS route.
        
        Args:
            path (str): The URL path for the route.
            **kwargs: Additional keyword arguments for the route.
            
        Returns:
            Callable: The decorator function.
        """

        @wraps(self.document("OPTIONS", path, **kwargs))
        def decorator(func):
            self.router.add_route(
                "OPTIONS",
                path,
                self.document("OPTIONS", path, **kwargs)(func),
                **kwargs,
            )
            return func

        return decorator

    def head(self, path: str, **kwargs):
        """
        Decorator to add a HEAD route.
        
        Args:
            path (str): The URL path for the route.
            **kwargs: Additional keyword arguments for the route.
            
        Returns:
            Callable: The decorator function.
        """

        @wraps(self.document("HEAD", path, **kwargs))
        def decorator(func):
            self.router.add_route(
                "HEAD", path, self.document("HEAD", path, **kwargs)(func), **kwargs
            )
            return func

        return decorator

    def trace(self, path: str, **kwargs):
        """
        Decorator to add a TRACE route.
        
        Args:
            path (str): The URL path for the route.
            **kwargs: Additional keyword arguments for the route.
            
        Returns:
            Callable: The decorator function.
        """

        @wraps(self.document("TRACE", path, **kwargs))
        def decorator(func):
            self.router.add_route(
                "TRACE", path, self.document("TRACE", path, **kwargs)(func), **kwargs
            )
            return func

        return decorator

    def connect(self, path: str, **kwargs):
        """
        Decorator to add a CONNECT route.
        
        Args:
            path (str): The URL path for the route.
            **kwargs: Additional keyword arguments for the route.
            
        Returns:
            Callable: The decorator function.
        """

        @wraps(self.document("CONNECT", path, **kwargs))
        def decorator(func):
            self.router.add_route(
                "CONNECT",
                path,
                self.document("CONNECT", path, **kwargs)(func),
                **kwargs,
            )
            return func

        return decorator
