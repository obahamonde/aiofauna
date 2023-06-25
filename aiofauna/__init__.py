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




🚀 Introducing aiofauna: A full-stack framework built on top of Aiohttp, Pydantic and Fauna




🔥 Inspired by FastAPI focuses on Developer Experience, Productivity and Versatili




🌟 Featur




✅ Supports Python 3.7+, comes with an opinionated ODM (Object Document Mapper) out of the box for FaunaDB that abstracts out complex FQL expressions into pythonic, fully typed asynchronous methods for all CRUD operations.




✅ Performant and scalable: Built on top of Aiohttp a powerful http server and client and FaunaDB an scalable serverless database for modern applications.




✅ Async/await coroutines: Leverage the power of async programming for enhanced performance and responsiveness, being ASGI compliant is compatible with most async python frameworks.




✅ Automatic Swagger UI generation: Automatic generation of interactive Swagger UI documentation for instant testing of your API.




✅ SSE (Server Sent Events): Built-in support for SSE (Server Sent Events) for real-time streaming of data from FaunaDB to your application.




✅ Robust data validation: Built-in support for Pydantic models for robust data validation and serialization.




✅ Auto-provisioning: Automatic management of indexes, unique indexes, and collections with FaunaModel ODM.




✅ Full JSON communication: Custom encoder to ensure seamless data exchange between your application and FaunaDB backend.




✅ Markdown and Jinja support with live reload: experiment an smooth frontend devserver experience without leaving your backend code.




✅ Inspired by fastapi, you will work with almost the same syntax and features like path operations, path parameters, query parameters, request body, status codes and more.




💡 With aiofauna, you can build fast, scalable, and reliable modern applications, while building seamless integrations thanks to the fastest http client aiohttp and the most versatile database FaunaDB, you will enjoy integrating with third party services such as APIs, Data Sources and Cloud Servic




📚 Check out the aiofauna library, and start building your next-gen applications toda




#Python #FaunaDB #Async #Pydantic #aiofauna




⚙️ If you are using a synchronous framework check out [Faudantic](https://github.com/obahamonde/faudantic) for a similar experience with FaunaDB and Pydantic.




📚 [Documentation](https://obahamonde-aiofauna-docs.smartpro.solutions) (Built with aiofau




📦 [PyPi](https://pypi.org/project/aiofaun




📦 [GitHub](https://github.com/obahamonde/aiofau




📦 [Demo](https://aiofaunastreams-fwuw7gz7oq-uc.a.run.app/) (Real time Latency Monitoring between FaunaDB and Google Cloud R


)


"""


from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union

from aiohttp.web import Request, Response
from aiohttp.web_request import FileField
from aiohttp.web_ws import WebSocketResponse
from aiohttp_sse import EventSourceResponse
from pydantic import BaseConfig  # pylint: disable=no-name-in-module
from pydantic import BaseModel  # pylint: disable=no-name-in-module
from pydantic import BaseSettings

from . import query as q
from .api import Api, HTTPException
from .asgi import ASGIApi
from .client import ApiClient, FaunaClient
from .fields import Field
from .helpers import aio, asyncify, make_response, redirect
from .json import FaunaJSONEncoder as JSONEncoder
from .json import _parse_json_hook as default
from .json import parse_json as loads
from .json import to_json as dumps
from .odm import FaunaModel
