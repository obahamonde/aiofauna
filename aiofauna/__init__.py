"""
README.md
"""

__version__ = "0.0.9"
__author__ = "obahamonde"
__license__ = "MIT"

import asyncio
from time import perf_counter
from datetime import datetime, date, time, timedelta
from typing import Any, AsyncGenerator, Callable, Dict, List, Optional, Union
from uuid import UUID, uuid4

from aiohttp.web import (
    Application,
    AppRunner,
    Request,
    Response,
    RouteDef,
    TCPSite,
    json_response,
)
from aiohttp.web_middlewares import middleware
from pydantic import (
    BaseModel,
    BaseSettings,
    BaseConfig,
    EmailStr,
    HttpUrl,
    validator,
)  # pylint: disable=no-name-in-module
from aiohttp_sse import sse_response
from aiofauna.client import ClientSession as AioSession, AsyncFaunaClient as AioClient
from aiofauna.errors import AioFaunaException as AioException
from aiofauna import query as q
from aiofauna.json import FaunaJSONEncoder, to_json
from aiofauna.odm import AsyncFaunaModel as AioModel
from aiofauna.application import App as AioApp
from aiofauna.helpers import jsonify, redirect, render_template
from aiofauna.asgi import aioasgi
