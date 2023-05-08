import io

import os

from typing import Optional as O, Dict as D, Any as A, AsyncGenerator as AG

from aiohttp import ClientSession

from dotenv import load_dotenv

from .errors import AioFaunaException

from .objects import Expr


from .json import FaunaJSONEncoder

load_dotenv()


def to_json(obj: Expr) -> str:
    """


    `to_json`


    Summary:


        Serialize a FaunaDB query.


    Args:


        obj: A FaunaDB query.


    Returns:


        A JSON string representing the FaunaDB query.
    """

    return FaunaJSONEncoder().encode(obj)


class AsyncFaunaClient(object):
    """


    `AsyncFaunaClient`


    Summary:


        Introducing support for coroutines and async/await syntax for FaunaDB python driver.


    Description:


        Using `_Expr` data type as an input for `AsyncFaunaClient.query` method.


        We can build fauna queries using `q` module methods and pass them to `AsyncFaunaClient.query` method


        as an instance of `_Expr` data type to execute them.


        The `_Expr` object will be serialized with `FaunaJSONEncoder` from json module so the FaunaDB API can understand it.


        The response will be deserialized by the `FaunaModel` class from orm module.
    """

    def __init__(self, secret=None):
        if secret is None:
            secret = os.getenv("FAUNA_SECRET")

        self.secret = secret

    async def query(self, expr: Expr) -> A:
        """


        `AsyncFaunaClient.query`


        Summary:


            Execute a FaunaDB query.



        Args:


            expr: A FaunaDB query.



        Returns:


            A FaunaDB response.
        """

        async with ClientSession() as session:
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

                except AioFaunaException as exc:
                    print(exc)

                    return None

    async def stream(self, expr: Expr) -> AG[A, None]:
        """

        `AsyncFaunaClient.stream`


        Summary:


                Streams a FaunaDB document.


        Args:


                expr: A FaunaDB query.


        Returns:


                An Event Stream Generator.
        """

        async with ClientSession() as session:
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


class HTTPClient:
    """

    Generic HTTP Client

    """

    async def fetch(
        self,
        url: str,
        method: str = "GET",
        headers: O[D[str, str]] = None,
        data: O[D[str, A]] = None,
    ) -> A:
        """
        Generic function to retrieve data from an URL in json format
        """
        if method in ["GET", "DELETE"]:
            async with ClientSession() as session:
                async with session.request(method, url, headers=headers) as response:
                    return await response.json()
        elif method in ["POST", "PUT", "PATCH"]:
            async with ClientSession() as session:
                async with session.request(
                    method, url, headers=headers, json=data
                ) as response:
                    return await response.json()
        else:
            raise ValueError("Invalid method")

    async def text(
        self,
        url: str,
        method: str = "GET",
        headers: O[D[str, str]] = None,
        data: O[D[str, A]] = None,
    ) -> str:
        """
        Generic function to retrieve data from an URL in text format
        """
        if method in ["GET", "DELETE"]:
            async with ClientSession() as session:
                async with session.request(method, url, headers=headers) as response:
                    return await response.text()
        elif method in ["POST", "PUT", "PATCH"]:
            async with ClientSession() as session:
                async with session.request(
                    method, url, headers=headers, json=data
                ) as response:
                    return await response.text()
        else:
            raise ValueError("Invalid method")

    async def blob(
        self,
        url: str,
        method: str = "GET",
        headers: O[D[str, str]] = None,
        data: O[D[str, A]] = None,
    ) -> bytes:
        """
        Generic function to retrieve data from an URL in binary format
        """
        if method in ["GET", "DELETE"]:
            async with ClientSession() as session:
                async with session.request(method, url, headers=headers) as response:
                    return await response.read()
        elif method in ["POST", "PUT", "PATCH"]:
            async with ClientSession() as session:
                async with session.request(
                    method, url, headers=headers, json=data
                ) as response:
                    return await response.read()
        else:
            raise ValueError("Invalid method")

    async def stream(
        self,
        url: str,
        method: str = "GET",
        headers: O[D[str, str]] = None,
        data: O[D[str, A]] = None,
    ) -> AG[str, None]:
        """
        Generic function to retrieve data from an URL in streaming format
        """
        if method in ["GET", "DELETE"]:
            async with ClientSession() as session:
                async with session.request(method, url, headers=headers) as response:
                    async for chunk in response.content.iter_chunked(1024):
                        yield chunk.decode("utf-8")
        elif method in ["POST", "PUT", "PATCH"]:
            async with ClientSession() as session:
                async with session.request(
                    method, url, headers=headers, json=data
                ) as response:
                    async for chunk in response.content.iter_chunked(1024):
                        yield chunk.decode("utf-8")
        else:
            raise ValueError("Invalid method")
