"""
Flaskaesque helper functions for aiohttp.
"""
import asyncio
from functools import wraps
from aiohttp import web
from aiohttp.web_request import FileField
from jinja2 import Environment, FileSystemLoader


def jsonify(func):
    """
    Decorator to convert the result of an asynchronous function to a JSON response.

    Args:
        func (callable): The asynchronous function to be wrapped.

    Returns:
        callable: A wrapped version of the input function that returns a JSON response.
    """

    @wraps(func)
    async def wrapper(request):
        try:
            return web.json_response(await func(request))
        except Exception as e:
            return web.json_response(func(request))

    return wrapper


def redirect(url):
    """
    Create an HTTP redirect response.

    Args:
        url (str): The URL to redirect to.

    Returns:
        web.HTTPFound: An HTTP redirect response with the specified URL.
    """
    return web.HTTPFound(url)


def make_response(data, headers=None, status=200):
    """
    Create an HTTP response with the given data, headers, and status code.

    Args:
        data (str): The response body data.
        headers (dict, optional): A dictionary of headers to include in the response. Defaults to None.
        status (int, optional): The HTTP status code for the response. Defaults to 200.

    Returns:
        web.Response: An HTTP response with the specified data, headers, and status code.
    """
    return web.Response(body=data, headers=headers, status=status)


def render_template(template_name, **kwargs):
    """
    Render an HTML template with the given context variables and return an HTTP response.

    Args
        template_name (str): The name of the template file.
        **kwargs: Keyword arguments representing context variables to be passed to the template.

    Returns:
        web.Response: An HTTP response with the rendered template as its body and content type set to "text/html".
    """
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template(template_name).render(**kwargs)
    return web.Response(body=template.encode(), content_type="text/html")


def upload_files(func):
    """
    Decorator to handler file uploading in an asynchronous function.

    Args:
        func (callable): The asynchronous function to be wrapped.

    Returns:
        callable: A wrapped version of the input function that returns a JSON response.
    """

    @wraps(func)
    async def wrapper(request: web.Request):
        file_payload = await request.post()
        files = {}
        for key, value in file_payload.items():
            if isinstance(value, FileField):
                files[key] = value
        if asyncio.iscoroutinefunction(func):
            return await func(request, files)
        return func(request, files)

    return wrapper
