from __future__ import annotations

import asyncio
from typing import Any, List, Type, TypeVar

from dotenv import load_dotenv
from pydantic import Field

from .client import FaunaClient
from .faunadb import query as q
from .faunadb.errors import FaunaException
from .json import JSONModel
from .utils import gen_emptystr, setup_logging

load_dotenv()

T = TypeVar("T", bound="FaunaModel")


class FaunaModel(JSONModel):
    ref: str = Field(default_factory=gen_emptystr)
    ts: str = Field(default_factory=gen_emptystr)

    class Metadata:
        subclasses: List[Type[FaunaModel]] = []

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.__doc__ is None:
            cls.__doc__ = f"```json\n{cls.schema_json(indent=2)}\n```"
        cls.Metadata.subclasses.append(cls)

    @classmethod
    @property
    def logger(cls):
        return setup_logging(cls.__name__)

    @classmethod
    async def create_all(cls):
        await asyncio.gather(*[model.provision() for model in cls.Metadata.subclasses])

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

        except (FaunaException, KeyError, TypeError, ValueError, Exception) as exc:
            cls.logger.error(exc.__class__.__name__)
            cls.logger.error(exc)

            return False

    @classmethod
    async def find_unique(cls: Type[T], **kwargs: Any) -> T:
        try:
            field, value = list(kwargs.items())[0]
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

        except (FaunaException, KeyError, TypeError, ValueError, Exception) as exc:
            cls.logger.error(exc.__class__.__name__)
            cls.logger.error(exc)
            return None  # type: ignore

    @classmethod
    async def find_many(cls: Type[T], limit: int = 50, **kwargs: Any) -> List[T]:
        try:
            _q = cls.q()
            field, value = list(kwargs.items())[0]
            refs = await _q(
                q.paginate(q.match(q.index(f"{cls.__name__.lower()}_{field}"), value))
            )
            refs = refs["data"][:limit]
            return await asyncio.gather(*[cls.get(item["@ref"]["id"]) for item in refs])

        except (FaunaException, KeyError, TypeError, ValueError, Exception) as exc:
            cls.logger.error(exc.__class__.__name__)
            cls.logger.error(exc)
            return []

    @classmethod
    async def get(cls: Type[T], ref: str) -> T:
        try:
            data = await cls.q()(q.get(q.ref(q.collection(cls.__name__.lower()), ref)))
            return cls(
                **{
                    **data["data"],  # type: ignore
                    "ref": data["ref"]["@ref"]["id"],  # type: ignore
                    "ts": data["ts"] / 1000,  # type: ignore
                }
            )

        except (FaunaException, KeyError, TypeError, ValueError, Exception) as exc:
            cls.logger.error(exc.__class__.__name__)
            cls.logger.error(exc)
            raise exc

    @classmethod
    async def all(cls: Type[T], limit: int = 100, offset: int = 0) -> List[T]:
        try:
            _q = cls.q()

            query = q.paginate(q.match(q.index(f"{cls.__name__.lower()}")))

            refs = (await _q(query))["data"][offset:limit]

            return await asyncio.gather(*[cls.get(item["@ref"]["id"]) for item in refs])

        except (FaunaException, KeyError, TypeError, ValueError, Exception) as exc:
            cls.logger.error(exc.__class__.__name__)
            cls.logger.error(exc)
            raise exc

    @classmethod
    async def delete_one(cls: Type[T], **kwargs: Any) -> bool:
        try:
            field, value = list(kwargs.items())[0]
            _q = cls.q()

            ref = await _q(
                q.get(q.match(q.index(f"{cls.__name__.lower()}_{field}_unique"), value))
            )

            await _q(q.delete(ref))

            return True

        except (FaunaException, KeyError, TypeError, ValueError, Exception) as exc:
            cls.logger.error(exc.__class__.__name__)
            cls.logger.error(exc)
            return False

    @classmethod
    async def delete(cls, ref: str) -> bool:
        try:
            await cls.q()(q.delete(q.ref(q.collection(cls.__name__.lower()), ref)))

            return True

        except (FaunaException, KeyError, TypeError, ValueError, Exception) as exc:
            cls.logger.error(exc.__class__.__name__)
            cls.logger.error(exc)
            return False

    async def create(self: T) -> T:
        try:
            for field in self.__fields__.values():
                if field.field_info.extra.get("unique"):
                    instance = await self.find_unique(
                        **{field.name: self.__dict__[field.name]}
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

        except (FaunaException, KeyError, TypeError, ValueError, Exception) as exc:
            self.logger.error(exc.__class__.__name__)
            self.logger.error(exc)
            raise exc

    @classmethod
    async def update(cls: Type[T], ref: str, **kwargs: Any) -> T:
        try:
            instance = await cls.q()(
                q.update(
                    q.ref(q.collection(cls.__name__.lower()), ref),
                    {"data": kwargs.get("kwargs", kwargs)},
                )
            )
            return cls(
                **{
                    **instance["data"],  # type: ignore
                    "ref": instance["ref"]["@ref"]["id"],  # type: ignore
                    "ts": instance["ts"] / 1000,  # type: ignore
                }
            )
        except (FaunaException, KeyError, TypeError) as exc:
            cls.logger.error(exc.__class__.__name__)
            cls.logger.error(exc)
            raise ValueError(f"Field {ref} not found")  # pylint: disable=all

    async def save(self: T) -> T:
        if isinstance(self.ref, str) and len(self.ref) == 18:
            return await self.update(self.ref, kwargs=self.dict())
        return await self.create()

    @classmethod
    async def cleanup(cls):
        await cls.client().cleanup()
