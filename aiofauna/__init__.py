"""
---
title: AioFauna
---

# AioFauna
 
 🚀 Introducing aiofauna: A full-stack framework for FaunaDB, industry performant with a seamless user experience! 🔥 Take your Backend Development to the next level dramatically improving productivity, performance and development experience.

🌟 Features:

✅ Inspired by FastAPI: DX (Developer Experience) first. Based on Pydantic, Aiohttp, and FaunaDB. CORS support, query and path parameters, request body parsing, most of the features you love from FastAPI are available in aiofauna.

✅ Blazingly Fast!: Industry performant http server while having the fastest python based http client allowing exceptional integrations with third party APIs, forget about installing dozens of SDKs.

✅ Async/await coroutines: Leverage the power of async programming for enhanced performance and responsiveness. 

✅ Automatic Swagger UI generation: Automatic documentation and manual testing UI following industry standard without further effort!.

✅ Live reload and SSE (Server-Sent Events) support: Stream data in real-time to your clients and experience effortless development with live reload.

✅ Pydantic-based Document Object Mapper (DOM): Define and validate your data models with ease. Summarize complex FQL expressions into pythonic, fully typed asynchronous methods for all CRUD operations.

✅ Auto-provisioning: Automatic management of indexes, unique indexes, and collections.

✅ Full JSON communication: Custom encoders to ensure seamless data exchange between your application and FaunaDB backend.

💡 With aiofauna, you can build fast, scalable, and reliable applications using the power of FaunaDB and modern asynchronous Python with its out of the box aiohttp based web framework. Say goodbye to the hassle of manually managing indexes and collections and hello to a seamless data driven development experience with FaunaModel.

🌐 aiofauna is independent and allows native interaction with external services like Docker API, GCP API, AWS API among others, implementing a lightweight stack with aiohttp server capabilities and fauna backend (to be enhanced soon).

📚 Check out the aiofauna library, and start building your next-gen applications today! 🚀
#Python #FaunaDB #Async #Pydantic #aiofauna

⚙️ If you are using a synchronous framework check out [Faudantic](https://github.com/obahamonde/faudantic) for a similar experience with FaunaDB and Pydantic.

📚 [Documentation](https://aiofauna.smartpro.solutions)

📦 [PyPi](https://pypi.org/project/aiofauna/)

📦 [GitHub](https://github.com/obahamonde/aiofauna)

📦 [Demo](https://aiofaunastreams-fwuw7gz7oq-uc.a.run.app/) (Stream data in real-time to your clients)

"""

__version__ = (0, 1, 0)
__author__ = "obahamonde"
__license__ = "MIT"

import json
from datetime import datetime
from typing import Any, AsyncGenerator, Callable, Dict, List, Optional, Union
from uuid import UUID, uuid4

import asyncio
import aiohttp_cors

from pydantic import BaseModel,BaseConfig, BaseSettings, Field  # pylint: disable=no-name-in-module

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
from aiohttp_sse import sse_response
from .client import ClientSession, AsyncFaunaClient as FaunaClient
from .errors import AioFaunaException as FaunaException
from . import query as q
from .json import (
    FaunaJSONEncoder as JSONEncoder,
    to_json as dumps,
    parse_json_or_none as loads,
)
from .odm import AsyncFaunaModel as FaunaModel
from .api import Api