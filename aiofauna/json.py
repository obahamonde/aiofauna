import asyncio
import base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
from datetime import date, datetime
from enum import Enum
from json import JSONEncoder, dumps, loads
from time import time
from typing import Any, Dict, List, Literal, TypeVar
from uuid import UUID

from iso8601 import parse_date
from pydantic import BaseModel  # pylint: disable=no-name-in-module
from typing_extensions import override

from .faunadb.objects import FaunaTime, Native, Query, Ref, SetRef
from .faunadb.query import Expr

T = TypeVar("T")

FaunaKey = Literal[
    "@ref", "@obj", "@set", "@query", "@ts", "@date", "@bytes", "@index", "@class"
]


def _parse_json_hook(dct: Dict[FaunaKey, Any]):
    if "@ref" in dct:
        ref = dct["@ref"]
        if not "collection" in ref and not "database" in ref:
            return Native.from_name(ref["id"])
        return Ref(ref["id"], ref.get("collection"), ref.get("database"))
    if "@obj" in dct:
        return dct["@obj"]
    if "@set" in dct:
        return SetRef(dct["@set"])
    if "@query" in dct:
        return Query(dct["@query"])
    if "@ts" in dct:
        return FaunaTime(dct["@ts"])
    if "@date" in dct:
        return parse_date(dct["@date"]).date()
    if "@bytes" in dct:
        return bytearray(urlsafe_b64decode(dct["@bytes"].encode()))
    return dct


def parse_json(json_string):
    try:
        return loads(json_string, object_hook=_parse_json_hook)
    except ValueError:
        pass


def to_json(dct, pretty=True, sort_keys=True):
    if pretty:
        return dumps(
            dct,
            cls=FaunaJSONEncoder,
            sort_keys=True,
            indent=4,
            separators=(", ", ": "),
            allow_nan=False,
            ensure_ascii=True,
        )
    return dumps(
        dct,
        cls=FaunaJSONEncoder,
        sort_keys=sort_keys,
        separators=(",", ":"),
        allow_nan=False,
        ensure_ascii=True,
    )


class FaunaJSONEncoder(JSONEncoder):
    @override
    def default(self, obj):
        if isinstance(obj, (Ref, SetRef, FaunaTime, Query)):
            return obj.to_fauna_json()
        if isinstance(obj, Expr):
            return obj.to_fauna_json()
        elif isinstance(obj, datetime):
            return obj.astimezone().isoformat()
        elif isinstance(obj, date):
            return {"@date": obj.isoformat()}
        elif isinstance(obj, (bytes, bytearray)):
            _val = None
            try:
                _val = obj.decode()
            except:
                _val = urlsafe_b64encode(obj).decode()  # pylint: disable=all
            return {"@bytes": _val}
        elif isinstance(obj, BaseModel):
            return obj.dict()
        elif isinstance(obj, Enum):
            return obj.value
        elif isinstance(obj, UUID):
            return {"@uuid": str(obj)}
        else:
            return super().default(obj)


class JSONModel(BaseModel):
    def to_dict(self, **kwargs):
        return parse_json(self.to_json(**kwargs))

    def to_json(self, **kwargs) -> str:
        return to_json(super().dict(**kwargs))

    @override
    def dict(self, **kwargs):
        return self.to_dict(**kwargs)

    @override
    def json(self, **kwargs) -> str:
        return self.to_json(**kwargs)


def jsonable_encoder(
    obj: Any,
    *,
    include: List[str] = [],
    exclude: List[str] = [],
    by_alias: bool = False,
    skip_defaults: bool = False,
    custom_encoder: Any = None,
) -> Any:
    """
    Convert any object to a JSON-serializable object.

    This function is used by Aiofauna to convert objects to JSON-serializable objects.

    It supports all the types supported by the standard json library, plus:

    * datetime.datetime
    * datetime.date
    * datetime.time
    * uuid.UUID
    * enum.Enum
    * pydantic.BaseModel
    """

    if custom_encoder is None:
        custom_encoder = FaunaJSONEncoder

    if obj is str:
        return "string"
    if obj is int or obj is float:
        return "integer"
    if obj is bool:
        return "boolean"
    if obj is None:
        return "null"
    if obj is list:
        return "array"
    if obj is dict:
        return "object"
    if obj is bytes:
        return "binary"
    if obj is datetime:
        return "date-time"
    if obj is date:
        return "date"
    if obj is time:
        return "time"
    if obj is UUID:
        return "uuid"
    if obj is Enum:
        return "enum"
    if isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    if isinstance(obj, (list, tuple, set, frozenset)):
        return [
            jsonable_encoder(
                v,
                include=include,
                exclude=exclude,
                by_alias=by_alias,
                skip_defaults=skip_defaults,
                custom_encoder=custom_encoder,
            )
            for v in obj
        ]
    if isinstance(obj, dict):
        return {
            jsonable_encoder(
                k,
                include=include,
                exclude=exclude,
                by_alias=by_alias,
                skip_defaults=skip_defaults,
                custom_encoder=custom_encoder,
            ): jsonable_encoder(
                v,
                include=include,
                exclude=exclude,
                by_alias=by_alias,
                skip_defaults=skip_defaults,
                custom_encoder=custom_encoder,
            )
            for k, v in obj.items()
        }
    if isinstance(obj, bytes):
        return base64.b64encode(obj).decode()
    if isinstance(obj, (set, frozenset)):
        return [
            jsonable_encoder(
                v,
                include=include,
                exclude=exclude,
                by_alias=by_alias,
                skip_defaults=skip_defaults,
                custom_encoder=custom_encoder,
            )
            for v in obj
        ]
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, UUID):
        return str(obj)
    if isinstance(obj, type):
        return jsonable_encoder(
            obj.__name__,
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            custom_encoder=custom_encoder,
        )

    return custom_encoder().default(obj)
