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

from .errors import FaunaException


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

    def __init__(self, **data: Any):
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
    def client(cls):
        fauna_secret = os.getenv("FAUNA_SECRET")

        return AsyncFaunaClient(secret=fauna_secret)

    @classmethod
    def q(cls):
        return cls.client().query

    @classmethod
    async def provision(cls):
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

                        print(cls.__name__.lower(), field.name)

                    print(
                        "Created unique index %s_%s", cls.__name__.lower(), field.name
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

        except( FaunaException, KeyError, TypeError) as exc:
            logging.error(exc)

            return False

    @classmethod
    async def exists(cls, ref: str):
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

        except( FaunaException, KeyError, TypeError) as exc:
            logging.error(exc)

            return False

    @classmethod
    async def find_unique(cls, field: str, value: Any):
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

        except( FaunaException, KeyError, TypeError) as exc:
            logging.error(exc)

            return None  # type: ignore # pylint: disable=unreachable

    @classmethod
    async def find_many(cls, field: str, value: Any):
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

        except( FaunaException, KeyError, TypeError) as exc:
            logging.error(exc)

            return []

    @classmethod
    async def get(cls, ref: str):
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

        except( FaunaException, KeyError, TypeError) as exc:
            logging.error(exc)

            return None  # type: ignore # pylint: disable=unreachable

    @classmethod
    async def all(cls, limit: int = 100, offset: int = 0):
        """
        Returns all documents of a collection.

        Parameters:
        -----------
        limit: int
            The maximum number of documents to return.
            
        offset: int
            The number of documents to skip.
            
        Returns:
        --------
        List[AsyncFaunaModel]:
            A list of instances of the model.
        """

        try:
            _q = cls.q()

            query = q.paginate(
                q.match(q.collection(cls.__name__.lower())), size=limit, after=offset
            )

            refs = (await _q(query))["data"]

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

        except( FaunaException, KeyError, TypeError) as exc:

            logging.error(exc)

            return []

    @classmethod
    async def delete_unique(cls, field: str, value: Any):
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

        except( FaunaException, KeyError, TypeError) as exc:
            logging.error(exc)

            return False

    @classmethod
    async def delete(cls, ref: str):
        """Delete a document by id"""

        try:
            await cls.q()(q.delete(q.ref(q.collection(cls.__name__.lower()), ref)))

            return True

        except( FaunaException, KeyError, TypeError) as exc:
            logging.error(exc)

            return False

    async def create(self):
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
                        field.name, self.__dict__[field.name]
                    )
                    if instance is None:
                        continue
                    if issubclass(instance.__class__, AsyncFaunaModel):
                        return instance
            data = await self.__class__.q()(
                q.create(
                    q.collection(self.__class__.__name__.lower()), {"data": self.dict()}
                )
            )
            self.ref = data["ref"]["@ref"]["id"]
            self.ts = data["ts"] / 1000
            return self

        except( FaunaException, KeyError, TypeError) as exc:
            logging.error(exc)

            return None  # type: ignore # pylint: disable=unreachable

    @classmethod
    async def query(cls, query: str):
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

        except( FaunaException, KeyError, TypeError) as exc:
            logging.error(exc)

            return []

    @classmethod
    async def update(cls, ref: str, **kwargs):
        try:
            instance = await cls.get(ref)
            if isinstance(instance, cls):
                instance_updated = await cls.q()(
                    q.update(
                        q.ref(q.collection(cls.__name__.lower()), ref),
                        {"data": kwargs.get("kwargs", kwargs)},
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
        except( FaunaException, KeyError, TypeError) as exc:
            logging.error(exc)
            raise ValueError(f"Field {ref} not found")

    async def save(self):
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

    @classmethod
    def gen_ts(cls):
        """Health check endpoint"""
        schema = cls.schema()
        ts_config = {}
        for name_, field in schema["properties"].items():
            if field.get("type") in ["string", "number", "boolean", "integer", "null"]:
                ts_config[name_] = (
                    field.get("type")
                    if name_ in schema["required"]
                    else f"{field['type']} | undefined"
                )
            elif field.get("type") == "array":
                if field.get("items").get("type") in [
                    "string",
                    "number",
                    "boolean",
                    "integer",
                    "null",
                ]:
                    ts_config[name_] = (
                        f"{field.get('items').get('type')}[]"
                        if name_ in schema["required"]
                        else f"{field.get('items').get('type')}[] | undefined"
                    )
                elif field.get("items").get("$ref"):
                    ts_config[name_] = (
                        f"{field.get('items').get('$ref').split('/')[-1]}[]"
                        if name_ in schema["required"]
                        else f"{field.get('items').get('$ref').split('/')[-1]}[] | undefined"
                    )
                elif field.get("items").get("object"):
                    ts_config[name_] = (
                        f"{field.get('items').get('title')}[]"
                        if name_ in schema["required"]
                        else f"{field.get('items').get('title')}[] | undefined"
                    )
            elif field.get("type") == "object":
                ts_config[name_] = (
                    field.get("title")
                    if name_ in schema["required"]
                    else f"{field.get('title')} | undefined"
                )
            elif field.get("$ref"):
                ts_config[name_] = (
                    field.get("$ref").split("/")[-1]
                    if name_ in schema["required"]
                    else f"{field.get('$ref').split('/')[-1]} | undefined"
                )
            elif field.get("object"):
                ts_config[name_] = (
                    field.get("title")
                    if name_ in schema["required"]
                    else f"{field.get('title')} | undefined"
                )
            elif field.get("oneOf"):
                ts_config[name_] = " | ".join(
                    [
                        f"{x.get('$ref').split('/')[-1]}"
                        if x.get("$ref")
                        else f"{x.get('title')}"
                        for x in field.get("oneOf")
                    ]
                )
            elif field.get("anyOf"):
                ts_config[name_] = " | ".join(
                    [
                        f"{x.get('$ref').split('/')[-1]}"
                        if x.get("$ref")
                        else f"{x.get('title')}"
                        for x in field.get("anyOf")
                    ]
                )
            elif field.get("allOf"):
                ts_config[name_] = " & ".join(
                    [
                        f"{x.get('$ref').split('/')[-1]}"
                        if x.get("$ref")
                        else f"{x.get('title')}"
                        for x in field.get("allOf")
                    ]
                )
            elif field.get("not"):
                ts_config[name_] = (
                    f"!{field.get('not').get('$ref').split('/')[-1]}"
                    if field.get("not").get("$ref")
                    else f"!{field.get('not').get('title')}"
                )
            elif field.get("enum"):
                ts_config[name_] = " | ".join([f"{x}" for x in field.get("enum")])
            else:
                ts_config[name_] = "any"

        ts_type = f"type {cls.__name__} = {ts_config}"

        return ts_type.replace("'", "")

    @classmethod
    def gen_store(cls):
        return f"""
        import {cls.__name__} from '~/types/{cls.__name__.lower()}'
        import {{ defineStore, acceptHMRUpdate }} from 'pinia'
        
        export const {cls.__name__}Store = defineStore('{cls.__name__.lower()}', () => {{
            const state = reactive({{
                {cls.__name__.lower()}s: [] as {cls.__name__}[],
                {cls.__name__.lower()}: null as {cls.__name__} | null,
                loading: false,
                error: null as string | null,
                notifications: [] as {{message: string, status: 'success' | 'error' | 'warning' | 'info'}}[]
            }})
            
            const api = {{
                async fetch{cls.__name__}s() {{  
                    state.loading = true
                    try {{
                        const {{ data }} =  await useFetch("/api/{cls.__name__.lower()}s").json()
                        state.{cls.__name__.lower()}s = unref(data)
                    }} catch (KeyError, TypeError) {{
                        state.error = error.message
                    }} finally {{
                        state.loading = false
                    }}
                }},
                async fetch{cls.__name__}(id: string) {{
                    state.loading = true
                    try {{
                        const {{ data }} =  await useFetch("/api/{cls.__name__.lower()}s/" + id).json()
                        state.{cls.__name__.lower()} = unref(data)
                    }} catch (KeyError, TypeError) {{
                        state.error = error.message
                    }} finally {{
                        state.loading = false
                    }}
                }},
                async create{cls.__name__}({cls.__name__.lower()}: {cls.__name__}) {{
                    state.loading = true
                    try {{
                        const {{ data }} =  await useFetch("/api/{cls.__name__.lower()}s", {{
                            method: "POST",
                            headers: {{
                                "Content-Type": "application/json"
                            }},
                            body: JSON.stringify({cls.__name__.lower()})
                        }}).json()
                        state.{cls.__name__.lower()} = unref(data)
                    }} catch (KeyError, TypeError) {{
                        state.error = error.message
                    }} finally {{
                        state.loading = false
                    }}
                }},
                async update{cls.__name__}({cls.__name__.lower()}: {cls.__name__}) {{
                    state.loading = true
                    try {{
                        const {{ data }} =  await useFetch("/api/{cls.__name__.lower()}s/" + {cls.__name__.lower()}.ref, {{
                            method: "PUT",
                            headers: {{
                                "Content-Type": "application/json"
                            }},
                            body: JSON.stringify({cls.__name__.lower()})
                        }}).json()
                        state.{cls.__name__.lower()} = unref(data)
                    }} catch (KeyError, TypeError) {{
                        state.error = error.message
                    }} finally {{
                        state.loading = false
                    }}
                }},
                async delete{cls.__name__}({cls.__name__.lower()}: {cls.__name__}) {{
                    state.loading = true
                    try {{
                        const {{ data }} =  await useFetch("/api/{cls.__name__.lower()}s/" + {cls.__name__.lower()}.ref, {{
                            method: "DELETE"
                        }}).json()
                        state.{cls.__name__.lower()} = unref(data)
                    }} catch (KeyError, TypeError) {{
                        state.error = error.message
                    }} finally {{
                        state.loading = false
                    }}
                }}
            }}

        
            return {{
                state,
                api
            }}
        }})
        
        if (import.meta.hot) {{
            import.meta.hot.accept(acceptHMRUpdate({cls.__name__}Store, import.meta.hot))
        }}
        """
