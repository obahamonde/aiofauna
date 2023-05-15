"""REST API Module with automatic OpenAPI generation."""
import json
import base64
import asyncio
from json import JSONDecoder
from typing import Any, Dict, List, Union
from inspect import signature
from uuid import UUID
from datetime import datetime, date, time
from functools import singledispatch
from enum import Enum
from aiohttp.web import Application, Request, Response, json_response
from aiohttp.web_request import FileField
from pydantic import BaseModel  # pylint: disable=no-name-in-module
from multidict import CIMultiDict
from .json import FaunaJSONEncoder, parse_json_or_none
from .odm import AsyncFaunaModel


class UploadFile(BaseModel):
    """
    File Upload Model
    """

    filename: str
    content_type: str
    data: bytes
    size: int
    headers: Dict[str, str]


def jsonable_encoder(
    obj: Any,
    *,
    include: List[str] = [],
    exclude: List[str] = [],
    by_alias: bool = False,
    skip_defaults: bool = False,
    custom_encoder: Any = None,
) -> Any:
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
        custom_encoder = FaunaJSONEncoder

    if obj is str:
        return "string"
    if obj is int or obj is float:
        return "integer"
    if obj is bool:
        return "boolean"
    if obj is None:
        return "null"
    if obj is list:
        return "array"
    if obj is dict:
        return "object"
    if obj is bytes:
        return "binary"
    if obj is datetime:
        return "date-time"
    if obj is date:
        return "date"
    if obj is time:
        return "time"
    if obj is UUID:
        return "uuid"
    if obj is Enum:
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


def extract_params(params: dict, path: str):
    """
    FastAPIesque function to extract the parameters of a function outside of the request context.
    """

    open_api_params = {}

    for name, param in params.items():
        type_ = param.annotation

        if type_ in (str, int, float, bool) and name:
            if f"{{{name}}}" in path:
                param_location = "path"
            else:
                param_location = "query"

            open_api_params[name] = {
                "in": param_location,
                "name": name,
                "required": True,
                "schema": {"type": type_, "default": param.default, "required": True},
            }

        elif type_ in [UploadFile, FileField]:
            open_api_params[name] = {
                "in": "formData",
                "name": name,
                "required": True,
                "schema": {"type": "file", "format": "binary"},
                "consumes": ["multipart/form-data"],
                "headers": {
                    "Content-Type": {"type": "string", "default": "multipart/form-data"}
                },
            }

        elif issubclass(type_, (BaseModel, AsyncFaunaModel)) and type_ != UploadFile:
            open_api_params[name] = {
                "in": "body",
                "name": name,
                "required": True,
                "schema": type_.schema(),
            }

        else:
            continue

    return open_api_params


def update_open_api(
    open_api: Dict[str, Any],
    path: str,
    method: str,
    func: Any,
    open_api_params: Dict[str, Any],
) -> None:
    if path in ["/openapi.json", "/docs"]:
        return

    _scalars = []
    _body = None
    _is_file_upload = False

    for param in open_api_params.values():
        if isinstance(param["schema"], dict):
            if "type" in param["schema"] and param["schema"]["type"] != "object":
                _scalars.append(param)
            else:
                _body = {"content": {"application/json": {"schema": param["schema"]}}}
        elif param["in"] == "formData" and param["schema"]["type"] == "file":
            _is_file_upload = True
            _scalars.append(param)
        else:
            continue

    if _body:
        open_api["paths"].setdefault(path, {})[method.lower()] = {
            "summary": func.__name__,
            "description": func.__doc__,
            "parameters": _scalars,
            "requestBody": _body
            if not _is_file_upload
            else {
                "content": {
                    "multipart/form-data": {
                        "schema": {
                            "properties": {
                                "file": {
                                    "type": "array",
                                    "items": {"type": "string", "format": "binary"},
                                }
                            }
                        }
                    }
                }
            },
            "responses": {"200": {"description": "OK"}},
        }
        open_api["components"]["schemas"].update(param["schema"])  # type: ignore
    else:
        open_api["paths"].setdefault(path, {})[method.lower()] = {
            "summary": func.__name__,
            "description": func.__doc__,
            "parameters": _scalars,
            "responses": {"200": {"description": "OK"}},
        }


async def inject_signature(request: Request, params: dict):
    """
    FastAPIesque function to shape the signature of a function to the request.
    """
    args_to_apply = {}

    for name, param in params.items():
        annotation = param.annotation
        if annotation in (str, int, float, bool) and name in request.match_info:
            args_to_apply[name] = request.match_info[name]
        elif annotation in (str, int, float, bool) and name in request.query:
            args_to_apply[name] = annotation(request.query[name])
        elif annotation in [FileField, UploadFile]:
            headers = dict(request.headers)
            new_headers = CIMultiDict(
                **headers, **{"content-type": "multipart/form-data"}
            )
            new_request = request.clone(headers=new_headers)
            args_to_apply[name] = new_request
        elif issubclass(annotation, BaseModel):
            data = await request.json(loads=JSONDecoder().decode)
            if isinstance(data, (str, bytes)):
                data = json.loads(data, object_hook=parse_json_or_none)
            args_to_apply[name] = annotation(**data)
        else:
            args_to_apply[name] = request
    return args_to_apply


@singledispatch
def do_response(response: Any) -> Response:
    """
    Flask-esque function to make a response from a function.
    """
    return response


@do_response.register(BaseModel)
def _(response: BaseModel) -> Response:
    return Response(
        status=200, body=json.dumps(response.dict()), content_type="application/json"
    )


@do_response.register(AsyncFaunaModel)
def _(response: AsyncFaunaModel) -> Response:
    response.ref = str(response.ref)
    return Response(
        status=200, body=json.dumps(response.dict()), content_type="application/json"
    )


@do_response.register(dict)
def _(response: dict) -> Response:
    return Response(
        status=200, body=json.dumps(response), content_type="application/json"
    )


@do_response.register(str)
def _(response: str) -> Response:
    return Response(status=200, body=response.encode(), content_type="text/plain")


@do_response.register(bytes)
def _(response: bytes) -> Response:
    return Response(status=200, body=response, content_type="application/octet-stream")


@do_response.register(int)
def _(response: int) -> Response:
    return Response(status=200, body=str(response).encode(), content_type="text/plain")


@do_response.register(float)
def _(response: float) -> Response:
    return Response(status=200, body=str(response).encode(), content_type="text/plain")


@do_response.register(bool)
def _(response: bool) -> Response:
    return Response(status=200, body=str(response).encode(), content_type="text/plain")


@do_response.register(list)
def _(
    response: List[Union[AsyncFaunaModel, BaseModel, dict, str, int, float]]
) -> Response:
    processed_response = []

    for item in response:
        if issubclass(item.__class__, BaseModel):
            processed_response.append(item.dict())  # type: ignore
        else:
            processed_response.append(item)

    return Response(
        status=200, body=json.dumps(processed_response), content_type="application/json"
    )


class Api(Application):
    """

    Api class to create a fastapi-like api.

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
            return json_response(response)

        @self.get("/docs")
        async def docs():
            html = f"""<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>AioFauna</title>
                <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.20.3/swagger-ui.css" >
                <link rel="icon" type="image/png" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.20.3/favicon-32x32.png" sizes="32x32" />
                <link rel="icon" type="image/png" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.20.3/favicon-16x16.png" sizes="16x16" />
                <style>
                html
                {{
                    box-sizing: border-box;
                    overflow: -moz-scrollbars-vertical;
                    overflow-y: scroll;
                }}
                
                .swagger-ui .topbar
                {{
                    display: none;
                }}
                    
                    
                *,
                *:before,
                *:after
                {{
                    box-sizing: inherit;
                }}

                body
                {{
                    margin:0;
                    background: #fafafa;
                }}
                </style>
            </head>

            <body>
                <div id="swagger-ui"></div>

                <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.20.3/swagger-ui-bundle.js"> </script>
                <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.20.3/swagger-ui-standalone-preset.js"> </script>
                <script>
                window.onload = function() {{
                const ui = SwaggerUIBundle({{
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
                }})
                window.ui = ui
                }}
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
            open_api_params = extract_params(params.copy(), path)
            self._route_open_api_params[(path, method)] = open_api_params
            update_open_api(self.openapi, path, method, func, open_api_params)

            async def wrapper(*args, **kwargs):
                request: Request = args[0]
                args = args[1:]
                args_to_apply = await inject_signature(request, params.copy())
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
            if event not in ["startup", "shutdown"]:
                raise ValueError("Event must be startup or shutdown")
            elif event == "startup":
                self.on_startup.append(func)
            else:
                self.on_shutdown.append(func)
            return func

        return decorator
