"""
README.md
"""

__version__ = "0.1.0"
__author__ = "@obahamonde [GitHub]"
__license__ = "MIT"

import asyncio
from datetime import datetime
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
from pydantic import BaseConfig  # pylint: disable=no-name-in-module
from pydantic import (
    BaseModel,
    BaseSettings,
    EmailStr,
    HttpUrl,
    validator,
)  # pylint: disable=no-name-in-module
from aiofauna import query as q
from aiofauna.client import AsyncFaunaClient as Client
from aiofauna.client import ClientSession
from aiofauna.errors import AioFaunaException
from aiofauna.json import FaunaJSONEncoder, to_json
from aiofauna.odm import AsyncFaunaModel as Model
from aiofauna.odm import Field, env
from aiofauna.streams import EventSourceResponse, sse_response
