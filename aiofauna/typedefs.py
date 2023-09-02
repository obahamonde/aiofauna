from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from enum import Enum
from typing import (Any, Callable, Dict, Generic, Iterable, List, Type,
                    TypeVar, Union, cast)
from uuid import UUID

from pydantic import BaseConfig  # pylint: disable=no-name-in-module
from pydantic import BaseModel  # pylint: disable=no-name-in-module
from pydantic import Extra  # pylint: disable=no-name-in-module
from pydantic import Field as PydanticField
from typing_extensions import ParamSpec

from .faunadb.objects import FaunaTime, Ref

Vector = List[float]

MetaData = Dict[str, str]

Undefined = Union[None, type(...), type(Ellipsis)]
NoArgAnyCallable = Callable[[], Any]

T = TypeVar("T")
P = ParamSpec("P")


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
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.__doc__ is None:
            cls.__doc__ = f"```json\n{cls.schema_json(indent=2)}\n```"
        cls.Metadata.subclasses.append(cls)


D = TypeVar("D", bound=Document)


class LazyProxy(Generic[T], ABC):
    def __init__(self) -> None:
        self.__proxied: T | None = None

    def __getattr__(self, attr: str) -> object:
        return getattr(self.__get_proxied__(), attr)

    def __repr__(self) -> str:
        return repr(self.__get_proxied__())

    def __str__(self) -> str:
        return str(self.__get_proxied__())

    def __dir__(self) -> Iterable[str]:
        return self.__get_proxied__().__dir__()

    def __get_proxied__(self) -> T:
        proxied = self.__proxied
        if proxied is not None:
            return proxied

        self.__proxied = proxied = self.__load__()
        return proxied

    def __set_proxied__(self, value: T) -> None:
        self.__proxied = value

    def __as_proxied__(self) -> T:
        """Helper method that returns the current proxy, typed as the loaded object"""
        return cast(T, self)

    @abstractmethod
    def __load__(self) -> T:
        ...


def Field(
    default: Any = Undefined,
    *,
    default_factory: NoArgAnyCallable | None = None,
    alias: str | None = None,
    title: str | None = None,
    description: str | None = None,
    const: bool | None = None,
    gt: float | None = None,
    ge: float | None = None,
    lt: float | None = None,
    le: float | None = None,
    multiple_of: float | None = None,
    allow_inf_nan: bool | None = None,
    max_digits: int | None = None,
    decimal_places: int | None = None,
    min_items: int | None = None,
    max_items: int | None = None,
    unique_items: bool | None = None,
    min_length: int | None = None,
    max_length: int | None = None,
    allow_mutation: bool = True,
    regex: str | None = None,
    discriminator: str | None = None,
    repr: bool = True,
    index: bool | None = None,
    unique: bool | None = None,
    **extra: Any,
) -> Any:
    """
        Used to provide extra information about a field, either for the model schema or complex validation. Some arguments apply only to number fields (int, float, Decimal) and some apply only to str.

    :param default: since this is replacing the field’s default, its first argument is used
      to set the default, use ellipsis (...) to indicate the field is required
    :param default_factory: callable that will be called when a default value is needed for this field
      If both default and default_factory are set, an error is raised.
    :param alias: the public name of the field
    :param title: can be any string, used in the schema
    :param description: can be any string, used in the schema
    :param exclude: exclude this field while dumping.
      Takes same values as the include and exclude arguments on the .dict method.
    :param include: include this field while dumping.
      Takes same values as the include and exclude arguments on the .dict method.
    :param const: this field is required and *must* take it's default value
    :param gt: only applies to numbers, requires the field to be "greater than". The schema
      will have an exclusiveMinimum validation keyword
    :param ge: only applies to numbers, requires the field to be "greater than or equal to". The
      schema will have a minimum validation keyword
    :param lt: only applies to numbers, requires the field to be "less than". The schema
      will have an exclusiveMaximum validation keyword
    :param le: only applies to numbers, requires the field to be "less than or equal to". The
      schema will have a maximum validation keyword
    :param multiple_of: only applies to numbers, requires the field to be "a multiple of". The
      schema will have a multipleOf validation keyword
    :param allow_inf_nan: only applies to numbers, allows the field to be NaN or infinity (+inf or -inf),
        which is a valid Python float. Default True, set to False for compatibility with JSON.
    :param max_digits: only applies to Decimals, requires the field to have a maximum number
      of digits within the decimal. It does not include a zero before the decimal point or trailing decimal zeroes.
    :param decimal_places: only applies to Decimals, requires the field to have at most a number of decimal places
      allowed. It does not include trailing decimal zeroes.
    :param min_items: only applies to lists, requires the field to have a minimum number of
      elements. The schema will have a minItems validation keyword
    :param max_items: only applies to lists, requires the field to have a maximum number of
      elements. The schema will have a maxItems validation keyword
    :param unique_items: only applies to lists, requires the field not to have duplicated
      elements. The schema will have a uniqueItems validation keyword
    :param min_length: only applies to strings, requires the field to have a minimum length. The
      schema will have a minLength validation keyword
    :param max_length: only applies to strings, requires the field to have a maximum length. The
      schema will have a maxLength validation keyword
    :param allow_mutation: a boolean which defaults to True. When False, the field raises a TypeError if the field is
      assigned on an instance. The BaseModel Config must set validate_assignment to True
    :param regex: only applies to strings, requires the field match against a regular expression
      pattern string. The schema will have a pattern validation keyword
    :param discriminator: only useful with a (discriminated a.k.a. tagged) Union of sub models with a common field.
      The discriminator is the name of this common field to shorten validation and improve generated schema
    :param repr: show this field in the representation
    :param **extra: any additional keyword arguments will be added as is to the schema
    """
    return PydanticField(
        default=default,
        default_factory=default_factory,
        alias=alias,
        title=title,
        description=description,
        const=const,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        multiple_of=multiple_of,
        allow_inf_nan=allow_inf_nan,
        max_digits=max_digits,
        decimal_places=decimal_places,
        min_items=min_items,
        max_items=max_items,
        unique_items=unique_items,
        min_length=min_length,
        max_length=max_length,
        allow_mutation=allow_mutation,
        regex=regex,
        discriminator=discriminator,
        repr=repr,
        index=index,
        unique=unique,
        **extra,
    )
