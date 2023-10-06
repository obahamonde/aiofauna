from __future__ import annotations

from datetime import date, datetime, time, timedelta
from decimal import Decimal
from enum import Enum
from typing import Any, List, Type, TypeVar
from uuid import UUID

from pydantic import BaseConfig  # pylint: disable=no-name-in-module
from pydantic import BaseModel  # pylint: disable=no-name-in-module
from pydantic import Extra  # pylint: disable=no-name-in-module

from ..faunadb.objects import FaunaTime, Ref


class Document(BaseModel):
    """Document
    Base document for all FaunaDB documents
    """

    class Config(BaseConfig):
        """Configuration defaults for all documents"""

        extra = Extra.allow
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.astimezone().isoformat(),
            date: lambda v: v.isoformat(),
            time: lambda v: v.isoformat(),
            timedelta: lambda v: v.total_seconds(),
            UUID: lambda v: str(v),
            Decimal: lambda v: float(v),
            Ref: lambda v: v.id(),
            FaunaTime: lambda v: v.value,
            Enum: lambda v: v.value,
        }

    class Metadata:
        subclasses: List[Type[Document]] = []

    @classmethod
    def __init_subclass__(cls, **kwargs: Any):
        super().__init_subclass__(**kwargs)
        if cls.__doc__ is None:
            cls.__doc__ = f"```json\n{cls.schema_json(indent=2)}\n```"
        cls.Metadata.subclasses.append(cls)


D = TypeVar("D", bound=Document)
