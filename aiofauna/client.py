import io


from typing import Any, AsyncGenerator, Optional


from aiohttp import ClientSession


from aiofauna.errors import AioFaunaException


from aiofauna.objects import Expr


from aiofauna.json import FaunaJSONEncoder


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

    secret: str

    def __init__(self, secret: Optional[str] = None) -> None:

        if secret is None:

            try:

                import os
                from dotenv import load_dotenv

                load_dotenv()

                self.secret = os.environ["FAUNA_SECRET"]

            except AioFaunaException as exc:

                print(
                    "Please provide a secret key or set the FAUNA_SECRET environment variable."
                )

                print(exc)

                return None

    async def query(self, expr: Expr) -> Any:
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

    async def stream(self, expr: Expr) -> AsyncGenerator[Any, None]:
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
