from __future__ import annotations

import asyncio
import logging
import os
from collections import defaultdict
from typing import Any, List, Optional, Type, TypeVar

try:
    import query as q

except ImportError:
    from . import query as q

from dotenv import load_dotenv
from pydantic import BaseModel  # pylint: disable=no-name-in-module

from .client import FaunaClient
from .errors import FaunaException
from .json import JSONModel

load_dotenv()

T = TypeVar("T")

Model = Type[T]

MaybeModel = Optional[Model]

ModelList = List[Model]


class Fql(BaseModel):
    field: str

    operator: str

    value: Any


class FaunaModel(JSONModel):
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

            except Exception:
                continue

    @classmethod
    def client(cls) -> FaunaClient:
        fauna_secret = os.getenv("FAUNA_SECRET")
        return FaunaClient(secret=fauna_secret)

    @classmethod
    def q(cls):
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

        except (FaunaException, KeyError, TypeError) as exc:
            logging.error(exc)

            return False

    @classmethod
    async def exists(cls, ref: str) -> bool:
        try:
            return await cls.q()(
                q.exists(q.ref(q.collection(cls.__name__.lower()), ref))
            )

        except (FaunaException, KeyError, TypeError) as exc:
            logging.error(exc)

            return False

    @classmethod
    async def find_unique(cls, field: str, value: Any) -> MaybeModel:
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

        except (FaunaException, KeyError, TypeError) as exc:
            logging.error(exc)
            return

    @classmethod
    async def find_many(cls, field: str, value: Any) -> ModelList:
        try:
            _q = cls.q()

            refs = (
                await _q(
                    q.paginate(
                        q.match(q.index(f"{cls.__name__.lower()}_{field}"), value)
                    )
                )
            )["data"]

            collection_refs_map = defaultdict(list)

            for ref in refs:
                collection = q.collection(cls.__name__.lower())

                collection_refs_map[collection].append(
                    q.ref(collection, ref["@ref"]["id"])
                )

            data = await asyncio.gather(
                *[
                    _q(q.get(q.paginate(collection_refs)))
                    for _, collection_refs in collection_refs_map.items()
                ]
            )

            flattened_data = [
                item for collection_data in data for item in collection_data["data"]
            ]

            return [
                cls(
                    **{**d["data"], "ref": d["ref"]["@ref"]["id"], "ts": d["ts"] / 1000}
                )
                for d in flattened_data
            ]

        except (FaunaException, KeyError, TypeError) as exc:
            logging.error(exc)

            return []

    @classmethod
    async def get(cls, ref: str) -> MaybeModel:
        try:
            data = await cls.q()(q.get(q.ref(q.collection(cls.__name__.lower()), ref)))
            return cls(
                **{
                    **data["data"],
                    "ref": data["ref"]["@ref"]["id"],
                    "ts": data["ts"] / 1000,
                }
            )

        except (FaunaException, KeyError, TypeError) as exc:
            logging.error(exc)
            return

    @classmethod
    async def all(cls) -> ModelList:
        try:
            _q = cls.q()

            query = q.paginate(q.match(q.index(f"{cls.__name__.lower()}")))

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

        except (FaunaException, KeyError, TypeError) as exc:
            logging.error(exc)

            return []

    @classmethod
    async def delete_unique(cls, field: str, value: Any) -> bool:
        try:
            _q = cls.q()

            ref = await _q(
                q.get(q.match(q.index(f"{cls.__name__.lower()}_{field}_unique"), value))
            )

            await _q(q.delete(ref))

            return True

        except (FaunaException, KeyError, TypeError) as exc:
            logging.error(exc)

            return False

    @classmethod
    async def delete(cls, ref: str) -> bool:
        try:
            await cls.q()(q.delete(q.ref(q.collection(cls.__name__.lower()), ref)))

            return True

        except (FaunaException, KeyError, TypeError) as exc:
            logging.error(exc)

            return False

    async def create(self) -> MaybeModel:
        try:
            for field in self.__fields__.values():
                if field.field_info.extra.get("unique"):
                    instance = await self.find_unique(
                        field.name, self.__dict__[field.name]
                    )

                    if instance is None:
                        continue

                    if issubclass(instance.__class__, FaunaModel):
                        return instance

            data = await self.__class__.q()(
                q.create(
                    q.collection(self.__class__.__name__.lower()), {"data": self.dict()}
                )
            )

            self.ref = data["ref"]["@ref"]["id"]

            self.ts = data["ts"] / 1000
            return self

        except (FaunaException, KeyError, TypeError) as exc:
            logging.error(exc)
            return

    @classmethod
    async def query(cls, query: str) -> ModelList:
        try:
            refs = (await cls.q()(q.paginate(q.match(q.query(query)))))["data"]

            data = await asyncio.gather(*[cls.q()(q.get(ref)) for ref in refs])

            return [
                cls(
                    **{**d["data"], "ref": d["ref"]["@ref"]["id"], "ts": d["ts"] / 1000}
                )
                for d in data
            ]

        except (FaunaException, KeyError, TypeError) as exc:
            logging.error(exc)

            return []

    @classmethod
    async def update(cls, ref: str, **kwargs) -> MaybeModel:
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

        except (FaunaException, KeyError, TypeError) as exc:
            logging.error(exc)

            raise ValueError(f"Field {ref} not found")

    async def save(self) -> MaybeModel:
        if isinstance(self.ref, str) and len(self.ref) == 18:
            return await self.update(self.ref, kwargs=self.dict())

        return await self.create()
