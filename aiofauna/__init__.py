"""
---
title: AioFauna
---

# AioFauna

 🚀 Introducing aiofauna: A powerful library to supercharge your FaunaDB experience with modern async Python frameworks! 🔥

🌟 Features:

✅ Async/await coroutines: Leverage the power of async programming for enhanced 
performance and responsiveness.

✅ SSE (Server-Sent Events) support: Stream data in real-time to your clients.

✅ Pydantic-based Document Object Mapper (DOM): Define and validate your data models with ease.

✅ Auto-provisioning: Automatic management of indexes, unique indexes, and collections.

✅ Standardized CRUD operations: Simplify your interactions with FaunaDB using find, find_unique, find_many, find_all, create, upsert, delete, and query methods.

✅ Full JSON communication: Custom encoders to ensure seamless data exchange between your application and FaunaDB backend.

✅ ASGI compliant: `aiofauna.asgi` module provides a middleware to convert `aiohttp.web.Application` into an ASGI application.

💡 With aiofauna, you can build fast, scalable, and reliable applications using the power of FaunaDB and modern asynchronous Python with its out of the box `aiohttp` based web framework. Say goodbye to the hassle of manually managing indexes and collections and hello to a seamless data driven development experience with Pydantic.

🌐 aiofauna is independent and allows native interaction with external services like Docker API, GCP API, AWS API among others, implementing a lightweight stack with aiohttp server capabilities and fauna backend (to be enhanced soon).

📚 Check out the aiofauna library, and start building your next-gen applications today! 🚀
#Python #FaunaDB #Async #Pydantic #aiofauna

⚙️  If you are using a synchronous framework check out [Faudantic](https://github.com/obahamonde/faudantic) for a similar experience with FaunaDB and Pydantic.

📚 [Documentation](https://aiofauna.smartpro.solutions)

📦 [PyPi](https://pypi.org/project/aiofauna/)

📦 [GitHub](https://github.com/obahamonde/aiofauna)

📦 [Demo](https://aiofaunastreams-fwuw7gz7oq-uc.a.run.app/) (Stream data in real-time to your clients) 

"""

__version__ = "0.0.11"
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
from aiofauna.helpers import jsonify, redirect, render_template, make_response, upload_files
from aiofauna.asgi import aioasgi
from aiofauna.datastructures import Graph
from aiofauna.api import Api