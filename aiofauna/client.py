import base64
import io
import os
from typing import Any, AsyncGenerator, Dict, List, Literal, Optional, Union

from aiohttp import ClientSession
from dotenv import load_dotenv

from .errors import FaunaException
from .json import to_json
from .objects import Expr
from .typedefs import LazyProxy

load_dotenv()

Method = Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
Json = Union[Dict[str, Any], List[Dict[str, Any]]]
MaybeJson = Optional[Json]
Headers = Dict[str, str]
MaybeHeaders = Optional[Headers]

class FaunaClient(LazyProxy[ClientSession]):
    def __init__(self, secret=None):
        if secret is None:
            secret = os.getenv("FAUNA_SECRET")
        self.secret = secret
        
    def __load__(self) -> ClientSession:
        return ClientSession()
    
    async def query(self, expr: Expr) -> MaybeJson:
        async with self.__load__() as session:
            async with session.post(
                "https://db.fauna.com",
                data=to_json(expr),
                headers={
                    "Authorization": f"Bearer {self.secret}",
                    "Content-type": "application/json",
                    "Accept": "application/json",
                },
            ) as response:
                try:
                    data = await response.json()

                    return data["resource"]

                except (
                    FaunaException,
                    ValueError,
                    KeyError,
                    TypeError,
                    Exception,
                ) as exc: # pylint:disable=all
                    return None

    async def stream(self, expr: Expr) -> AsyncGenerator[str, None]:
        async with self.__load__() as session:
            async with session.post(
                "https://db.fauna.com",
                data=to_json(expr),
                headers={
                    "Authorization": f"Bearer {self.secret}",
                    "Content-type": "application/json",
                    "Accept": "text/event-stream",
                    "Keep-Alive": "timeout=5, max=900",
                    "Connection": "keep-alive",
                    "Cache-Control": "no-cache",
                    "X-Last-Seen-Txn": "0",
                    "X-Request-By": "aiofauna",
                    "X-Query-By": "aiofauna",
                },
            ) as response:
                with io.StringIO() as buffer:
                    async for chunk in response.content.iter_chunked(1024):
                        buffer.write(chunk.decode())

                        buffer.seek(0)

                        for line in buffer:
                            if line == "\r\n":
                                yield buffer.getvalue()

                                buffer.seek(0)

                                buffer.truncate()

                            else:
                                yield line

class ApiClient(LazyProxy[ClientSession]):
    """

    Generic HTTP Client

    """
    
    def __init__(self, base_url:Optional[str]=None, headers:Optional[Headers]=None):
        super().__init__()
        self.base_url = base_url
        self.headers = headers
        
     
    def __load__(self) -> ClientSession:
        return ClientSession()

    async def fetch(self, url:str, method:Method="GET", headers:MaybeHeaders=None, json:MaybeJson=None) -> MaybeJson:
        if self.base_url is not None:
            url = self.base_url + url
        if self.headers is not None and headers is not None:
            headers = {**self.headers, **headers}
        elif self.headers is not None:
            headers = self.headers
        async with self.__load__() as session:
            async with session.request(method, url, headers=headers, json=json) as response:
                try:
                    data = await response.json()
                    return data
                except (
                    FaunaException,
                    ValueError,
                    KeyError,
                    TypeError,
                    Exception,
                ) as exc: # pylint:disable=broad-exception-caught, unused-variable
                    return None
                
    async def text(self, url:str, method:Method="GET", headers:MaybeHeaders=None, json:MaybeJson=None) -> Optional[str]:
        if self.base_url is not None:
            url = self.base_url + url
        if self.headers is not None and headers is not None:
            headers = {**self.headers, **headers}
        elif self.headers is not None:
            headers = self.headers
        async with self.__load__() as session:
            async with session.request(method, url, headers=headers, json=json) as response:
                try:
                    data = await response.text()
                    return data
                except (
                    FaunaException,
                    ValueError,
                    KeyError,
                    TypeError,
                    Exception,
                ) as exc: # pylint:disable=broad-exception-caught, unused-variable
                    return None # type: ignore
                
    async def stream(self, url:str, method:Method="GET", headers:MaybeHeaders=None, json:MaybeJson=None) -> AsyncGenerator[str, None]:
        if self.base_url is not None:
            url = self.base_url + url
        if self.headers is not None and headers is not None:
            headers = {**self.headers, **headers}
        elif self.headers is not None:
            headers = self.headers
        async with self.__load__() as session:
            async with session.request(method, url, headers=headers, json=json) as response:
                async for chunk in response.content.iter_chunked(1024):
                    try:
                        yield chunk.decode()
                    except (
                        FaunaException,
                        ValueError,
                        KeyError,
                        TypeError,
                        Exception,
                    ) as exc:
                        print(exc) # pylint:disable=broad-exception-caught
                        yield base64.b64encode(chunk).decode()