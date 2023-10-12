"""Automatically generate OpenAPI documentation for your AioFauna API."""
from inspect import Parameter
from json import JSONDecoder, loads
from typing import Any, Dict, List

from aiohttp.web import Request
from aiohttp.web_request import FileField
from pydantic import BaseModel  # pylint: disable=no-name-in-module

from ..data.json import parse_json


def extract(params: Dict[str, Parameter], path: str):
    """
    Extract OpenAPI parameters from the function parameters.

    Args:
        params (dict): The parameters of the function.
        path (str): The URL path of the endpoint.

    Returns:
        Dict[str, Any]: The extracted OpenAPI parameters.
    """
    open_api_params: Dict[str, Any] = {}

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
                "schema": {"type": type_},
            }

            if param.default is not param.empty:
                open_api_params[name]["schema"]["default"] = param.default

        elif type_ in [FileField]:
            open_api_params[name] = {
                "in": "formData",
                "name": name,
                "required": True,
                "schema": {"type": "file"},
                "consumes": "multipart/form-data"
            }

        elif issubclass(type_, (BaseModel)):
            open_api_params[name] = {
                "in": "body",
                "name": name,
                "required": True,
                "schema": type_.schema(),
            }

        else:
            continue

    return open_api_params


def transform(
    open_api: Dict[str, Any],
    path: str,
    method: str,
    func: Any,
    open_api_params: Dict[str, Any],
    tags: List[str] = [],
):
    """
    Update the OpenAPI documentation with the endpoint information.

    Args:
        open_api (Dict[str, Any]): The OpenAPI documentation.
        path (str): The URL path of the endpoint.
        method (str): The HTTP method of the endpoint.
        func (Any): The function being documented.
        open_api_params (Dict[str, Any]): The OpenAPI parameters of the function.
    """
    if path in ["/openapi.json", "/docs"]:
        return

    _scalars: List[Dict[str, Any]] = []
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

    route_info = {
        "summary": func.__name__,
        "description": func.__doc__,
        "parameters": _scalars,
        "responses": {"200": {"description": "OK"}},
    }

    if tags:
        route_info["tags"] = tags

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
                            "type": "object",
                            "properties": {
                                "file": {"type": "string", "format": "binary"}
                            },
                        }
                    }
                }
            },
            "responses": {"200": {"description": "OK"}},
        }

    else:
        open_api["paths"].setdefault(path, {})[method.lower()] = {
            "summary": func.__name__,
            "description": func.__doc__,
            "parameters": _scalars,
            "responses": {"200": {"description": "OK"}},
        }


async def load(request: Request, params: Dict[str, Parameter]):
    """
    Shape the endpoint function parameters to match the request.

    Args:
        request (Request): The HTTP request.
        params (dict): The parameters of the function.

    Returns:
        Dict[str, Any]: The updated parameters to apply to the function.
    """
    args_to_apply: Dict[str, Any] = {}

    for name, param in params.items():
        annotation = param.annotation
        if annotation in (str, int, float, bool) and name in request.match_info:
            args_to_apply[name] = request.match_info[name]
        elif annotation in (str, int, float, bool) and name in request.query:
            args_to_apply[name] = annotation(request.query[name])
        elif annotation == FileField:
            file = (await request.post()).get("file")
            assert isinstance(file, FileField), "File not found"
            args_to_apply[name] = file
        elif issubclass(annotation, BaseModel):
            data = await request.json(loads=JSONDecoder().decode)
            if isinstance(data, (str, bytes)):
                data = loads(data, object_hook=parse_json)  # type: ignore
            args_to_apply[name] = annotation(**data)
        else:
            args_to_apply[name] = request
    return args_to_apply


def html_string(base_url: str):
    """
    Returns a string with the html code to render the swagger ui
    """
    return f"""<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>AioFauna</title>
                <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css" >
                <link rel="icon" type="image/png" href="https://www.aiofauna.com/logo.png" sizes="32x32" />
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

                <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"> </script>
                <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-standalone-preset.js"> </script>
                <script>
                window.onload = function() {{
                const ui = SwaggerUIBundle({{
                    url: "{base_url}",
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
