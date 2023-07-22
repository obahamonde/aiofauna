from __future__ import annotations

import asyncio
import os
from collections import defaultdict
from datetime import datetime
from typing import Any, List, Optional, Type, TypeVar

from dotenv import load_dotenv
from pydantic import BaseModel  # pylint: disable=no-name-in-module
from pydantic.main import ModelMetaclass

from .client import FaunaClient
from .faunadb import query as q
from .faunadb.errors import FaunaException
from .json import JSONModel
from .logging import setup_logging

load_dotenv()

T = TypeVar("T", bound="FaunaModel")



class FaunaModelMetaclass(ModelMetaclass):
    def __new__(cls, name, bases, attrs):
        new_cls = super().__new__(cls, name, bases, attrs)
        cls.Metadata.__subclasses__.append(new_cls)
        return new_cls

    class Metadata:
        __subclasses__: List[Type[FaunaModel]] = []


class FaunaModel(JSONModel, metaclass=FaunaModelMetaclass):
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
    @property
    def logger(cls):
        return setup_logging(cls.__name__)

    @classmethod
    async def create_all(cls):
        await asyncio.gather(
            *[model.provision() for model in cls.Metadata.__subclasses__]
        )

    @classmethod
    def client(cls):
        return FaunaClient()

    @classmethod
    def q(cls):
        return cls.client().query

    @classmethod
    async def provision(cls) -> bool:
        _q = cls.q()

        try:
            if not await _q(q.exists(q.collection(cls.__name__.lower()))):
                await _q(q.create_collection({"name": cls.__name__.lower()}))

                cls.logger.info("Created collection %s", cls.__name__.lower())

            if not await _q(q.exists(q.index(cls.__name__.lower()))):
                await _q(
                    q.create_index(
                        {
                            "name": cls.__name__.lower(),
                            "source": q.collection(cls.__name__.lower()),
                        }
                    )
                )

                cls.logger.info("Created index %s", cls.__name__.lower())

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

                        cls.logger.info(
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

                        cls.logger.info(
                            "Created index %s_%s", cls.__name__.lower(), field.name
                        )
                        continue

            return True

        except (FaunaException, KeyError, TypeError) as exc:
            cls.logger.error(exc)

            return False

    @classmethod
    async def find_unique(cls: Type[T], field: str, value: Any) -> Optional[T]:
        try:
            data = await cls.q()(
                q.get(q.match(q.index(f"{cls.__name__.lower()}_{field}_unique"), value))
            )
            return cls(
                **{
                    **data["data"],  # type: ignore
                    "ref": data["ref"]["@ref"]["id"],  # type: ignore
                    "ts": data["ts"] / 1000,  # type: ignore
                }
            )

        except (FaunaException, KeyError, TypeError) as exc:
            cls.logger.error(exc)
            return None

    @classmethod
    async def find_many(cls: Type[T], field: str, value: Any) -> List[T]:
        try:
            _q = cls.q()

            refs = await _q(
                q.paginate(q.match(q.index(f"{cls.__name__.lower()}_{field}"), value))
            )

            assert isinstance(refs, dict)

            refs = refs["data"]

            collection_refs_map = defaultdict(list)

            for ref in refs:
                collection = q.collection(cls.__name__.lower())

                collection_refs_map[collection].append(
                    q.ref(collection, ref["@ref"]["id"])  # type: ignore
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
            cls.logger.error(exc)

            return []

    @classmethod
    async def get(cls: Type[T], ref: str) -> Optional[T]:
        try:
            data = await cls.q()(q.get(q.ref(q.collection(cls.__name__.lower()), ref)))
            return cls(
                **{
                    **data["data"],  # type: ignore
                    "ref": data["ref"]["@ref"]["id"],  # type: ignore
                    "ts": data["ts"] / 1000,  # type: ignore
                }
            )

        except (FaunaException, KeyError, TypeError) as exc:
            cls.logger.error(exc)
            return None

    @classmethod
    async def all(cls: Type[T]) -> List[T]:
        try:
            _q = cls.q()

            query = q.paginate(q.match(q.index(f"{cls.__name__.lower()}")))

            refs = (await _q(query))["data"]  # type: ignore

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
            cls.logger.error(exc)

            return []

    @classmethod
    async def delete_one(cls, field: str, value: Any) -> bool:
        try:
            _q = cls.q()

            ref = await _q(
                q.get(q.match(q.index(f"{cls.__name__.lower()}_{field}_unique"), value))
            )

            await _q(q.delete(ref))

            return True

        except (FaunaException, KeyError, TypeError) as exc:
            cls.logger.error(exc)

            return False

    @classmethod
    async def delete(cls, ref: str) -> bool:
        try:
            await cls.q()(q.delete(q.ref(q.collection(cls.__name__.lower()), ref)))

            return True

        except (FaunaException, KeyError, TypeError) as exc:
            cls.logger.error(exc)

            return False

    async def create(self: T) -> Optional[T]:
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

            self.ref = data["ref"]["@ref"]["id"]  # type: ignore

            self.ts = data["ts"] / 1000  # type: ignore
            return self

        except (FaunaException, KeyError, TypeError) as exc:
            self.logger.error(exc)
            return None

    @classmethod
    async def update(cls: Type[T], ref: str, **kwargs) -> T:
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
                        **instance_updated["data"],  # type: ignore
                        "ref": instance_updated["ref"]["@ref"]["id"],  # type: ignore
                        "ts": instance_updated["ts"] / 1000,  # type: ignore
                    }
                )

            else:
                raise ValueError(f"Field {ref} not found")

        except (FaunaException, KeyError, TypeError) as exc:
            cls.logger.error(exc)

            raise ValueError(f"Field {ref} not found")  # pylint: disable=all

    async def save(self: T) -> Optional[T]:
        if isinstance(self.ref, str) and len(self.ref) == 18:
            return await self.update(self.ref, kwargs=self.dict())

        return await self.create()

    @classmethod
    async def cleanup(cls):
        await cls.client().cleanup()