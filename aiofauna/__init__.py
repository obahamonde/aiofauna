"""




AioFauna




"""


__version__ = (0, 2, 0)


__author__ = "obahamonde"


__license__ = "MIT"


__doc__ = """
---
title: AioFauna
---

# AioFauna

🚀 Introducing aiofauna: A full-stack framework built on top of Aiohttp, Pydantic and FaunaDB.

🔥 Inspired by FastAPI focuses on Developer Experience, Productivity and Versatility.

🌟 Features:

✅ Supports Python 3.7+, comes with an opinionated ODM (Object Document Mapper) out of the box for FaunaDB that abstracts out complex FQL expressions into pythonic, fully typed asynchronous methods for all CRUD operations.

✅ Powerful and Scalable: Being built on top of Aiohttp an asyncio based http server/client and FaunaDB an scalable serverless database for modern applications allows for powerful and seamless integrations.

✅ Performant: As a framework built on top of Aiohttp it leverages the power of asyncio and the fastest python `APIClient` built on top of aiohttp with Lazy Loading and session sharing, plus the ubiquiness of FaunaDB to achieve high performance.

✅ Automatic Swagger UI generation: Automatic generation of interactive Swagger UI documentation for instant testing of your `APIServer`, exposed at the `/docs` path.

✅ SSE (Server Sent Events): Built-in support for SSE (Server Sent Events) for real-time streaming of data from FaunaDB to your application, syntactic sugar through the `@sse` decorator.

✅ Websockets: Built-in support for Websockets for real-time bidirectional communication between your application and the resources served by AioFauna `APIServer`, syntactic sugar through the `@websocket` decorator.

✅ Robust data validation: Utilizes the rich features of Pydantic for data validation and serialization.

✅ Auto-provisioning: Automatic management of indexes, unique indexes, and collections with `FaunaModel` ODM.

✅ Full JSON communication: Focus on your data, don't worry about the communication protocol. Your `APIServer` will receive and return JSON.

✅ APIRouter: AioFauna comes with a powerful APIRouter class that allows you to organize your `APIServer` endpoints with path operations, path parameters, query parameters, request body, status codes, and decorated view functions.

✅ Inspired by fastapi, you will work with almost the same syntax and features like path operations, path parameters, query parameters, request body, status codes, `/docs` automatic interactive API documentation, and decorated view functions and automatic serialization and deserialization of your data.

💡 With aiofauna, you can build fast, scalable, and reliable modern applications, avoiding decision fatigue and focusing on what really matters, your data and your business logic.

📚 Check out the aiofauna library, and start building your next-gen applications today! 🚀

#Python #FaunaDB #Async #Pydantic #aiofauna

⚙️ If you are using a synchronous framework check out [Faudantic](https://github.com/obahamonde/faudantic) for a similar experience with FaunaDB and Pydantic.

📦 [PyPi](https://pypi.org/project/aiofauna/)

📦 [Demo](https://natal-ia.netlify.app) (LLM smart agent)

📦 [GitHub](https://github.com/obahamonde/aiofauna)

"""


from typing import *  # pylint: disable=wildcard-import,unused-wildcard-import

from aiohttp.web_ws import WebSocketResponse
from aiohttp_sse import EventSourceResponse
from typing_extensions import ParamSpec

from .client import APIClient, FaunaClient
from .docs import FileField
from .faunadb import query as q
from .helpers import async_cpu, async_io, asyncio, template, component
from .json import FaunaJSONEncoder, parse_json, to_json
from .odm import FaunaModel
from .server import APIRouter, APIServer, Request, Response
from .typedefs import Document, Field, LazyProxy, Component
from .utils import chunker, handle_errors, process_time, setup_logging
from .markdown import md_component
