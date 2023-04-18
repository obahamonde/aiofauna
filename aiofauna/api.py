"""REST API Module with automatic OpenAPI generation."""
import os
import base64
import asyncio
from typing import (
    Any,
    Dict,
)
from inspect import signature
from uuid import UUID
from datetime import datetime, date, time
from enum import Enum
import aiohttp_cors
from aiohttp.web import (
    Application,
    Request,
    Response,
    json_response,
    AppRunner,
    TCPSite,
)
from aiohttp.web_request import FileField
from aiofauna.odm import AsyncFaunaModel as BaseModel
from aiofauna.json import FaunaJSONEncoder as JSONEncoder


def jsonable_encoder(
    obj,
    *,
    include=None,
    exclude=None,
    by_alias=False,
    skip_defaults=False,
    custom_encoder=None,
):
    """
    Convert any object to a JSON-serializable object.

    This function is used by Aiofauna to convert objects to JSON-serializable objects.

    It supports all the types supported by the standard json library, plus:
    
    * datetime.datetime
    * datetime.date
    * datetime.time
    * uuid.UUID
    * enum.Enum
    * pydantic.BaseModel
    
    """

    if custom_encoder is None:
        custom_encoder = JSONEncoder
    if obj == str:
        return "string"
    if obj in (int, float):
        return "number"
    if obj == bool:
        return "boolean"
    if obj == None:
        return "null"
    if obj == list:
        return "array"
    if obj == dict:
        return "object"
    if obj == bytes:
        return "binary"
    if obj == datetime:
        return "date-time"
    if obj == date:
        return "date"
    if obj == time:
        return "time"
    if obj == UUID:
        return "uuid"
    if obj == Enum:
        return "enum"
    if isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    if isinstance(obj, (list, tuple, set, frozenset)):
        return [
            jsonable_encoder(
                v,
                include=include,
                exclude=exclude,
                by_alias=by_alias,
                skip_defaults=skip_defaults,
                custom_encoder=custom_encoder,
            )
            for v in obj
        ]
    if isinstance(obj, dict):
        return {
            jsonable_encoder(
                k,
                include=include,
                exclude=exclude,
                by_alias=by_alias,
                skip_defaults=skip_defaults,
                custom_encoder=custom_encoder,
            ): jsonable_encoder(
                v,
                include=include,
                exclude=exclude,
                by_alias=by_alias,
                skip_defaults=skip_defaults,
                custom_encoder=custom_encoder,
            )
            for k, v in obj.items()
        }
    if isinstance(obj, bytes):
        return base64.b64encode(obj).decode()

    if isinstance(obj, (set, frozenset)):
        return [
            jsonable_encoder(
                v,
                include=include,
                exclude=exclude,
                by_alias=by_alias,
                skip_defaults=skip_defaults,
                custom_encoder=custom_encoder,
            )
            for v in obj
        ]
    if isinstance(obj, (datetime, date, time)):
        return obj.isoformat()
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, UUID):
        return str(obj)
    return custom_encoder().default(obj)


def extract_parameters_without_request(params: dict):

    """
    
    Helper function to extract parameters from a function without the request parameter.
    
    """

    open_api_params = {}

    for name, param in params.items():
        type_ = param.annotation

        if type_ in (str, int, float, bool):
            open_api_params[name] = {
                "in": "query",
                "name": name,
                "required": True,
                "schema": {"type": type_, "default": param.default, "required": True},
            }

        elif issubclass(type_, BaseModel):
            open_api_params[name] = {
                "in": "body",
                "name": name,
                "required": True,
                "schema": {
                    "type": "object",
                    "default": param.default,
                    "required": True,
                },
            }

        elif issubclass(type_, FileField):
            open_api_params[name] = {
                "in": "formData",
                "name": name,
                "required": True,
                "schema": {"type": "file", "default": param.default, "required": True},
            }

        elif issubclass(type_, Request):
            continue

        else:
            continue

    return {}, open_api_params


def update_open_api(
    open_api: Dict[str, Any],
    path: str,
    method: str,
    func: Any,
    open_api_params: Dict[str, Any],
) -> None:

    """

    Helper function to update the open_api dictionary with the parameters of a function.
    
    """

    open_api["paths"].setdefault(path, {})[method.lower()] = {
        "summary": func.__name__,
        "description": func.__doc__,
        "parameters": list(open_api_params.values()),
        "responses": {"200": {"description": "OK"}},
    }


async def extract_parameters(request: Request, params: dict):

    """
    
    Helper function to extract parameters from a function.
    
    """

    args_to_apply = {}
    open_api_params = {}

    for name, param in params.items():
        type_ = param.annotation

        if type_ in (str, int, float, bool) and name in request.match_info:
            open_api_params[name] = {
                "in": "path",
                "name": name,
                "required": True,
                "schema": {"type": type_, "default": param.default, "required": True},
            }
            args_to_apply[name] = request.match_info[name]

        elif type_ in (str, int, float, bool) and name in request.query:
            open_api_params[name] = {
                "in": "query",
                "name": name,
                "required": True,
                "schema": {"type": type_, "default": param.default, "required": True},
            }
            args_to_apply[name] = type_(request.query[name])

        elif issubclass(type_, BaseModel):
            open_api_params[name] = {
                "in": "body",
                "name": name,
                "required": True,
                "schema": {
                    "type": "object",
                    "default": param.default,
                    "required": True,
                },
            }
            args_to_apply[name] = type_(**await request.json())

        elif issubclass(type_, FileField):
            open_api_params[name] = {
                "in": "formData",
                "name": name,
                "required": True,
                "schema": {"type": "file", "default": param.default, "required": True},
            }
            args_to_apply[name] = await request.post()

        elif issubclass(type_, Request):

            continue

        else:

            continue

    return args_to_apply, open_api_params


class Api(Application):
    """
    
    Api class to create a fastapi-like api.
    
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.openapi = {
            "openapi": "3.0.0",
            "info": {"title": "API", "version": "1.0.0"},
            "paths": {},
            "components": {},
        }
        self._route_open_api_params = {}

        @self.get("/openapi.json")
        async def openapi():
            response = jsonable_encoder(self.openapi)
            return json_response(response)

        @self.get("/docs")
        async def docs():
            html = """<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>AioFauna</title>
                <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.20.3/swagger-ui.css" >
                <link rel="icon" type="image/png" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.20.3/favicon-32x32.png" sizes="32x32" />
                <link rel="icon" type="image/png" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.20.3/favicon-16x16.png" sizes="16x16" />
                <style>
                html
                {
                    box-sizing: border-box;
                    overflow: -moz-scrollbars-vertical;
                    overflow-y: scroll;
                }

                *,
                *:before,
                *:after
                {
                    box-sizing: inherit;
                }

                body
                {
                    margin:0;
                    background: #fafafa;
                }
                </style>
            </head>

            <body>
                <div id="swagger-ui"></div>

                <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.20.3/swagger-ui-bundle.js"> </script>
                <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.20.3/swagger-ui-standalone-preset.js"> </script>
                <script>
                window.onload = function() {
                // Begin Swagger UI call region
                const ui = SwaggerUIBundle({
                    url: "/openapi.json",
                    dom_id: '#swagger-ui',
                    deepLinking: true,
                    presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                    ],
                    plugins: [
                    SwaggerUIBundle.plugins.DownloadUrl
                    ],
                    layout: "StandaloneLayout"
                })
                // End Swagger UI call region

                window.ui = ui
                }
            </script>
            </body>
            </html>
            """
            return Response(body=html.encode(), content_type="text/html")

    def document(self, path: str, method: str):

        """
        
        Decorator to document a function.
        
        """

        def decorator(func):
            sig = signature(func)
            params = sig.parameters
            _, open_api_params = extract_parameters_without_request(params.copy())
            self._route_open_api_params[(path, method)] = open_api_params
            update_open_api(self.openapi, path, method, func, open_api_params)

            async def wrapper(*args, **kwargs):
                request: Request = args[0]
                args = args[1:]
                args_to_apply, _ = await extract_parameters(request, params.copy())
                if asyncio.iscoroutinefunction(func):
                    return await func(*args, **kwargs, **args_to_apply)
                return func(*args, **kwargs, **args_to_apply)

            wrapper._handler = func
            return wrapper

        return decorator

    def get(self, path: str, **kwargs):
        def decorator(func):
            self.router.add_get(path, self.document(path, "GET")(func), **kwargs)
            return func

        return decorator

    def post(self, path: str, **kwargs):
        def decorator(func):
            self.router.add_post(path, self.document(path, "POST")(func), **kwargs)
            return func

        return decorator

    def put(self, path: str, **kwargs):
        def decorator(func):
            self.router.add_put(path, self.document(path, "PUT")(func), **kwargs)
            return func

        return decorator

    def delete(self, path: str, **kwargs):
        def decorator(func):
            self.router.add_delete(path, self.document(path, "DELETE")(func), **kwargs)
            return func

        return decorator

    def patch(self, path: str, **kwargs):
        def decorator(func):
            self.router.add_patch(path, self.document(path, "PATCH")(func), **kwargs)
            return func

        return decorator

    def head(self, path: str, **kwargs):
        def decorator(func):
            self.router.add_head(path, self.document(path, "HEAD")(func), **kwargs)
            return func

        return decorator

    def options(self, path: str, **kwargs):
        def decorator(func):
            self.router.add_options(
                path, self.document(path, "OPTIONS")(func), **kwargs
            )
            return func

        return decorator

    def static(self, path: str, directory: str, **kwargs):
        def decorator(func):
            self.router.add_static(path, directory, **kwargs)
            return func

        return decorator

    async def listen(self, host: str = "0.0.0.0", port: int = 8000, **kwargs):

        cors = aiohttp_cors.setup(
            self,
            defaults={
                "*": aiohttp_cors.ResourceOptions(
                    allow_credentials=True, expose_headers="*", allow_headers="*",
                )
            },
        )
        for route in list(self.router.routes()):
            cors.add(route)
            handler = route.handler._handler  # pylint: disable=protected-access
            path = route.resource.canonical  # type: ignore
            method = route.method.lower()
            open_api_params = self._route_open_api_params.get((path, method), {})
            update_open_api(self.openapi, path, method, handler, open_api_params)

        runner = AppRunner(self)

        await runner.setup()

        site = TCPSite(runner, host, port)

        await site.start()

        print(f"http://{host}:{port}/docs")

        while True:

            await asyncio.sleep(3600)
