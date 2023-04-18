import asyncio
from typing import Callable, Any, Awaitable, Union, List, Dict, Optional, Type, TypeVar, cast, overload
from aiohttp.web import Application, Request, Response, json_response
from aiohttp.web_request import FileField
from aiofauna.odm import AsyncFaunaModel as BaseModel
from aiofauna import AioModel as Model

from inspect import signature

def create_open_api_params():
    return {
        "title": "Aiofauna",
        "version": "0.0.1",
        "openapi": "3.0.0",
        "paths": {}}

def update_open_api(open_api: Dict[str, Any], path: str, method: str, func: Any, open_api_params: Dict[str, Any]) -> None:
    # Ensure the required keys are present in the open_api dictionary"
    open_api["paths"].setdefault(path, {})[method.lower()] = {
        "summary": func.__name__,
        "description": func.__doc__,
        "parameters": list(open_api_params.values()),
        "responses": {
            "200": {
                "description": "OK"
            }
        }
    }
    
    
async def extract_parameters(request:Request, params:dict):
    args_to_apply = {}
    open_api_params = {}
    
    for name, param in params.items():
        type_ = param.annotation
        
        if type_ in (str,int,float,bool) and name in request.match_info:
            open_api_params[name] = {
                "in": "path",
                "name": name,
                "required": True,
                "schema": {
                    "type": type_.__name__,
                    "default": param.default,
                    "required": True
                
            }
        }
            args_to_apply[name] = request.match_info[name]

            
        elif type_ in (str,int,float,bool) and name in request.query:
            open_api_params[name] = {
                "in": "query",
                "name": name,
                "required": True,
                "schema": {
                    "type": type_.__name__,
                    "default": param.default,
                    "required": True
                }
            }
            args_to_apply[name] = type_(request.query[name])

        elif issubclass(type_, Model):
            open_api_params[name] = {
                "in": "body",
                "name": name,
                "required": True,
                "schema": {
                    "type": "object",
                    "default": param.default,
                    "required": True
                }
            }
            args_to_apply[name] = type_(**await request.json())
            
        elif issubclass(type_, FileField):
            open_api_params[name] = {
                "in": "formData",
                "name": name,
                "required": True,
                "schema": {
                    "type": "file",
                    "default": param.default,
                    "required": True
                }
            }
            args_to_apply[name] = await request.post()
            
        elif issubclass(type_, Request):
            
            continue
        
        else:
            
            continue
        
    return args_to_apply, open_api_params

class Api(Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.openapi = create_open_api_params()

    def document(self, path:str, method:str):
        def decorator(func):
            async def wrapper(*args, **kwargs) -> Response:
                sig = signature(func)
                params = sig.parameters
                request:Request = args[0]
                args = args[1:]
                args_to_apply, open_api_params = await extract_parameters(request, params.copy())
                
                update_open_api(self.openapi, path, method, func, open_api_params)
                if asyncio.iscoroutinefunction(func):
                    return await func(*args, **args_to_apply, **kwargs)
                return func(*args, **args_to_apply, **kwargs)
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
            self.router.add_options(path, self.document(path, "OPTIONS")(func), **kwargs)
            return func
        return decorator
    
    def static(self, path: str, directory: str, **kwargs):
        def decorator(func):
            self.router.add_static(path, directory, **kwargs)
            return func
        return decorator
        
    