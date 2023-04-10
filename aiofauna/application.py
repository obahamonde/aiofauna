from __future__ import annotations
import jinja2
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
        self.jinja_env.variable_start_string = "${"
        self.jinja_env.variable_end_string = "}"
        self.jinja_env.auto_reload = True

    def route(self, method: str, path: str, **kwargs):
        """
        Decorator to define a route and its corresponding handler function.

        Args:
            method (str): The HTTP method for the route (e.g., "GET", "POST").
            path (str): The URL path for the route.
            **kwargs: Additional keyword arguments for the route.

        Returns:
            Callable: The decorator function.
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            self.router.add_route(method, path, wrapper, **kwargs)
            return wrapper

        return decorator

    def get(self, path: str, **kwargs):

        """
        
        Decorator to define a GET route and its corresponding handler function.
        
        Args:
            path (str): The URL path for the route.
            **kwargs: Additional keyword arguments for the route.
            
        Returns:
        
            Callable: The decorator function.
            
        """

        return self.route("GET", path, **kwargs)

    def post(self, path: str, **kwargs):

        """

        Decorator to define a POST route and its corresponding handler function.
        
        Args:
            path (str): The URL path for the route.
            **kwargs: Additional keyword arguments for the route.
            
        Returns:
        
            Callable: The decorator function.
            
        """

        return self.route("POST", path, **kwargs)

    def put(self, path: str, **kwargs):

        """
        
        Decorator to define a PUT route and its corresponding handler function.
        
        
        Args:
            path (str): The URL path for the route.
            **kwargs: Additional keyword arguments for the route.
            
            
        Returns:
        
            Callable: The decorator function.
        
        """
        return self.route("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs):

        """
        
        Decorator to define a PATCH route and its corresponding handler function.
        
        Args:
            path (str): The URL path for the route.
            **kwargs: Additional keyword arguments for the route.
            
            
        Returns:
        
            Callable: The decorator function.
        
        """

        return self.route("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs):

        """

        Decorator to define a DELETE route and its corresponding handler function.
        
        Args:
            path (str): The URL path for the route.
            **kwargs: Additional keyword arguments for the route.
            
            
        Returns:    
            Callable: The decorator function.
            
        """
        return self.route("DELETE", path, **kwargs)

    def options(self, path: str, **kwargs):

        """
        
        Decorator to define an OPTIONS route and its corresponding handler function.
        
        Args:
            path (str): The URL path for the route.
            **kwargs: Additional keyword arguments for the route.
            
        Returns:
            
            Callable: The decorator function.
                
            """

        return self.route("OPTIONS", path, **kwargs)

    def head(self, path: str, **kwargs):

        """
        
        Decorator to define a HEAD route and its corresponding handler function.
        
        Args:
            path (str): The URL path for the route.
            **kwargs: Additional keyword arguments for the route.
            
        Returns:
        
            Callable: The decorator function.
            
        """
        return self.route("HEAD", path, **kwargs)

    def connect(self, path: str, **kwargs):

        """
        
        Decorator to define a CONNECT route and its corresponding handler function.
        
        Args:
            path (str): The URL path for the route.
            **kwargs: Additional keyword arguments for the route.
            
        
        Returns:
            
                Callable: The decorator function.
                
            """

        return self.route("CONNECT", path, **kwargs)

    def trace(self, path: str, **kwargs):

        """
        
        Decorator to define a TRACE route and its corresponding handler function.
        
        
        Args:
            path (str): The URL path for the route.
            **kwargs: Additional keyword arguments for the route.
            
            
        Returns:
        
            Callable: The decorator function.
            
        """

        return self.route("TRACE", path, **kwargs)

    def add(self, method: str, path: str, func: Callable, **kwargs):

        """
        
        Add a route and its corresponding handler function.
        
        Args:
            method (str): The HTTP method for the route (e.g., "GET", "POST").
            path (str): The URL path for the route.
            func (Callable): The handler function for the route.
            **kwargs: Additional keyword arguments for the route.
            
        """

        self.router.add_route(method, path, func, **kwargs)
        return self

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
