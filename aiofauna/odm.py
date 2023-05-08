"""Lightweight ORM to perform simple CRUD operations on FaunaDB collections and provision indexes


   the fauna query object is available also within the class for further customization
"""


from __future__ import annotations


import logging

import os

import asyncio


from typing import List, Optional, Any, Callable, Union

try:
    import query as q  # type: ignore
except ImportError:
    from . import query as q

from .errors import AioFaunaException


from .json import JSONModel  # pylint: disable=no-name-in-module


from .client import AsyncFaunaClient


from pydantic import BaseModel  # pylint: disable=no-name-in-module


from dotenv import load_dotenv


load_dotenv()


class Fql(BaseModel):
    field: str

    operator: str

    value: Any


class AsyncFaunaModel(JSONModel):
    """

    FaunaDB Base Model
    """

    ref: Optional[str] = None

    ts: Optional[str] = None

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

        for field in self.__fields__.values():
            try:
                one_of = field.field_info.extra.get("oneOf")

                if isinstance(one_of, list):
                    if data.get(field.name) not in one_of:
                        raise ValueError(f"{field.name} must be one of {one_of}")

            except Exception:  # pylint: disable=broad-except
                continue

    @classmethod
    def client(cls) -> AsyncFaunaClient:
        fauna_secret = os.getenv("FAUNA_SECRET")

        return AsyncFaunaClient(secret=fauna_secret)

    @classmethod
    def q(cls) -> Callable:
        return cls.client().query

    @classmethod
    async def provision(cls) -> bool:
        _q = cls.q()
        try:
            if not await _q(q.exists(q.collection(cls.__name__.lower()))):
                await _q(q.create_collection({"name": cls.__name__.lower()}))

                print("Created collection %s", cls.__name__.lower())

            if not await _q(q.exists(q.index(cls.__name__.lower()))):
                await _q(
                    q.create_index(
                        {
                            "name": cls.__name__.lower(),
                            "source": q.collection(cls.__name__.lower()),
                        }
                    )
                )

                print(f"Created index {cls.__name__.lower()}")

            for field in cls.__fields__.values():
                if field.field_info.extra.get("unique"):
                    if not await _q(
                        q.exists(q.index(f"{cls.__name__.lower()}_{field.name}_unique"))
                    ):
                        await _q(
                            q.create_index(
                                {
                                    "name": f"{cls.__name__.lower()}_{field.name}_unique",
                                    "source": q.collection(cls.__name__.lower()),
                                    "terms": [{"field": ["data", field.name]}],
                                    "unique": True,
                                }
                            )
                        )

                        print(
                            cls.__name__.lower(),
                            field.name,
                        )

                    print(
                        "Created unique index %s_%s",
                        cls.__name__.lower(),
                        field.name,
                    )

                    continue

                if field.field_info.extra.get("index"):
                    if not await _q(
                        q.exists(q.index(f"{cls.__name__.lower()}_{field.name}"))
                    ):
                        await _q(
                            q.create_index(
                                {
                                    "name": f"{cls.__name__.lower()}_{field.name}",
                                    "source": q.collection(cls.__name__.lower()),
                                    "terms": [{"field": ["data", field.name]}],
                                }
                            )
                        )

                        print("Created index %s_%s", cls.__name__.lower(), field.name)
                        continue

            return True

        except AioFaunaException as exc:
            logging.error(exc)

            return False

    @classmethod
    async def exists(cls, ref: str) -> bool:
        """


        Checks if a document exists in FaunaDB.



        Parameters:
        -----------
        ref: int


            The reference ID of the document to check.



        Returns:
        --------


        bool:


            True if the document exists, False otherwise.
        """

        try:
            return await cls.q()(
                q.exists(q.ref(q.collection(cls.__name__.lower()), ref))
            )

        except AioFaunaException as exc:
            logging.error(exc)

            return False

    @classmethod
    async def find_unique(
        cls, field: str, value: Any
    ) -> Union[AsyncFaunaModel, BaseModel]:
        """


        Finds a document in FaunaDB by a unique field.



        Parameters:
        -----------
        field: str


            The name of the field to search.


        value: Any


            The value to search for.



        Returns:
        --------


        Union[AsyncFaunaModel,BaseModel]:


            An instance of the model if found, None otherwise.
        """

        try:
            data = await cls.q()(
                q.get(q.match(q.index(f"{cls.__name__.lower()}_{field}_unique"), value))
            )
            return cls(
                **{
                    **data["data"],
                    "ref": data["ref"]["@ref"]["id"],
                    "ts": data["ts"] / 1000,
                }
            )

        except AioFaunaException as exc:
            logging.error(exc)

            raise ValueError(f"{field} {value} not found")

    @classmethod
    async def find_many(cls, field: str, value: Any) -> List[AsyncFaunaModel]:
        """


        Finds documents in FaunaDB by a field.



        Parameters:
        -----------
        field: str


            The name of the field to search.


        value: Any


            The value to search for.



        Returns:
        --------


        List[AsyncFaunaModel]:


            A list of instances of the model if found, None otherwise.
        """

        try:
            _q = cls.q()

            refs = (
                await _q(
                    q.paginate(
                        q.match(q.index(f"{cls.__name__.lower()}_{field}"), value)
                    )
                )
            )["data"]

            data = await asyncio.gather(
                *[
                    _q(
                        q.get(
                            q.ref(q.collection(cls.__name__.lower()), ref["@ref"]["id"])
                        )
                    )
                    for ref in refs
                ]
            )

            return [
                cls(
                    **{**d["data"], "ref": d["ref"]["@ref"]["id"], "ts": d["ts"] / 1000}
                )
                for d in data
            ]

        except AioFaunaException as exc:
            logging.error(exc)

            return []

    @classmethod
    async def find(cls, ref: str) -> Union[AsyncFaunaModel, BaseModel]:
        """


        Finds a document in FaunaDB by its ID.



        Parameters:
        -----------
        ref: int


            The reference ID of the document to find.



        Returns:
        --------


        Union[AsyncFaunaModel,BaseModel]:


            An instance of the model if found, None otherwise.
        """

        try:
            data = await cls.q()(q.get(q.ref(q.collection(cls.__name__.lower()), ref)))
            return cls(
                **{
                    **data["data"],
                    "ref": data["ref"]["@ref"]["id"],
                    "ts": data["ts"] / 1000,
                }
            )

        except AioFaunaException as exc:
            logging.error(exc)

            raise ValueError(f"{ref} not found")

    @classmethod
    async def all(cls) -> List[AsyncFaunaModel]:
        """


        Finds all documents of the model in FaunaDB.



        Returns:
        --------


        List[AsyncFaunaModel]:


            A list of instances of the model if found, None otherwise.
        """

        try:
            _q = cls.q()

            refs = (await _q(q.paginate(q.match(q.index(cls.__name__.lower())))))[
                "data"
            ]

            data = await asyncio.gather(
                *[
                    _q(
                        q.get(
                            q.ref(q.collection(cls.__name__.lower()), ref["@ref"]["id"])
                        )
                    )
                    for ref in refs
                ]
            )

            return [
                cls(
                    **{**d["data"], "ref": d["ref"]["@ref"]["id"], "ts": d["ts"] / 1000}
                )
                for d in data
            ]

        except AioFaunaException as exc:
            logging.error(exc)

            return []

    @classmethod
    async def delete_unique(cls, field: str, value: Any) -> bool:
        """


                Deletes a document in FaunaDB by a unique field.



                Parameters:
                -----------
                field: str


                    The name of the unique field to use in the search.


                value: Any


                    The value of the unique field to use in the search.



                Returns:
                --------


                bool:
        t

                    True if the document is deleted, False otherwise.
        """

        try:
            _q = cls.q()

            ref = await _q(
                q.get(q.match(q.index(f"{cls.__name__.lower()}_{field}_unique"), value))
            )

            await _q(q.delete(ref))

            return True

        except AioFaunaException as exc:
            logging.error(exc)

            return False

    @classmethod
    async def delete(cls, ref: str) -> bool:
        """Delete a document by id"""

        try:
            await cls.q()(q.delete(q.ref(q.collection(cls.__name__.lower()), ref)))

            return True

        except AioFaunaException as exc:
            logging.error(exc)

            return False

    async def create(self) -> AsyncFaunaModel:
        """


        Creates a new document in FaunaDB.



        Parameters:
        -----------


        **kwargs:


            The data to create the new document with.



        Returns:
        --------


        Union[AsyncFaunaModel,BaseModel]:


            An instance of the model if created successfully, None otherwise.
        """

        try:
            for field in self.__fields__.values():
                if field.field_info.extra.get("unique"):
                    instance = await self.find_unique(
                        field.name, getattr(self, field.name)
                    )
                    if instance is None:
                        continue
                    await instance.__class__.q()(q.create(q.collection(self.__class__.__name__.lower()), {"data": self.dict()}))  # type: ignore
                    return instance  # type: ignore
            data = await self.__class__.q()(
                q.create(
                    q.collection(self.__class__.__name__.lower()), {"data": self.dict()}
                )
            )
            self.ref = data["ref"]["@ref"]["id"]
            self.ts = data["ts"] / 1000
            return self

        except AioFaunaException as exc:
            logging.error(exc)

            raise ValueError(exc)

    @classmethod
    async def query(cls, query: str) -> List[AsyncFaunaModel]:
        """


        Queries FaunaDB using a string query and returns a list of instances of the model.



        Args:


            query (str): The query to use.



        Returns:


            List[AsyncFaunaModel]: A list of instances of the model if found, None otherwises.
        """

        try:
            refs = (await cls.q()(q.paginate(q.match(q.query(query)))))["data"]

            data = await asyncio.gather(*[cls.q()(q.get(ref)) for ref in refs])

            return [
                cls(
                    **{**d["data"], "ref": d["ref"]["@ref"]["id"], "ts": d["ts"] / 1000}
                )
                for d in data
            ]

        except AioFaunaException as exc:
            logging.error(exc)

            return []

    @classmethod
    async def update(cls, ref: str, **kwargs) -> AsyncFaunaModel:
        try:
            instance = await cls.find(ref)
            if isinstance(instance, cls):
                instance_updated = await cls.q()(
                    q.update(
                        q.ref(q.collection(cls.__name__.lower()), ref), {"data": kwargs}
                    )
                )
                return cls(
                    **{
                        **instance_updated["data"],
                        "ref": instance_updated["ref"]["@ref"]["id"],
                        "ts": instance_updated["ts"] / 1000,
                    }
                )
            else:
                raise ValueError(f"Field {ref} not found")
        except AioFaunaException as exc:
            logging.error(exc)
            raise ValueError(f"Field {ref} not found")

    async def save(self) -> AsyncFaunaModel:
        """


        Saves a document in FaunaDB.



        Returns:
        --------


        Union[AsyncFaunaModel,BaseModel]:


            An instance of the model if saved successfully, None otherwise.
        """

        if isinstance(self.ref, str) and len(self.ref) == 18:
            return await self.update(self.ref, kwargs=self.dict())
        return await self.create()
