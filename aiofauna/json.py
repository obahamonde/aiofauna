import asyncio
from base64 import urlsafe_b64decode, urlsafe_b64encode
from datetime import date, datetime
from json import JSONEncoder, dumps, loads
from typing import overload
from typing_extensions import override
from iso8601 import parse_date
from pydantic import BaseModel
from aiofauna.objects import FaunaTime, Native, Query, Ref, SetRef
from aiofauna.query import Expr
from aiohttp.web import Request, Response


def parse_json(json_string):
    return loads(json_string, object_hook=_parse_json_hook)


def parse_json_or_none(json_string):
    try:
        return parse_json(json_string)
    except ValueError:
        pass


def _parse_json_hook(dct):
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


def to_json(dct, pretty=True, sort_keys=True):
    if pretty:
        return dumps(
            dct, cls=FaunaJSONEncoder, sort_keys=True, indent=4, separators=(", ", ": ")
        )
    return dumps(dct, cls=FaunaJSONEncoder, sort_keys=sort_keys, separators=(",", ":"))


class FaunaJSONEncoder(JSONEncoder):
    @override
    def default(self, obj):
        if isinstance(obj, (Ref, SetRef, FaunaTime, Query)):
            return obj.to_fauna_json()
        if isinstance(obj, Expr):
            return obj.to_fauna_json()
        elif isinstance(obj, datetime):
            return FaunaTime(obj).to_fauna_json()
        elif isinstance(obj, date):
            return {"@date": obj.isoformat()}
        elif isinstance(obj, (bytes, bytearray)):
            return {"@bytes": urlsafe_b64encode(obj).decode("utf-8")}
        elif isinstance(obj, BaseModel):
            return obj.dict()
        elif isinstance(obj, Request):
            if obj.content_type in (
                "application/json",
                "application/x-www-form-urlencoded",
            ):
                data = parse_json_or_none(obj.content.read_nowait().decode())
                if data:
                    return {
                        "method": obj.method,
                        "path": obj.path,
                        "headers": dict(obj.headers),
                        "body": data,
                    }
            elif obj.content_type == "multipart/form-data":
                data = {}
                for (k, v) in asyncio.run(obj.post()):
                    _v = None
                    try:
                        _v = loads(v)
                    except ValueError:
                        _v = "file"
                    data[k] = v
            else:
                data = None
                return {
                    "method": obj.method,
                    "query_params": dict(obj.query),
                    "path_params": dict(obj.match_info),
                    "headers": dict(obj.headers),
                    "body": data,
                }


class JSONModel(BaseModel):
    def to_dict(self, **kwargs):
        return parse_json_or_none(self.to_json(**kwargs))

    def to_json(self, **kwargs) -> str:
        return to_json(super().dict(**kwargs))

    @override
    def dict(self, **kwargs):
        return self.to_dict(**kwargs)

    @override
    def json(self, **kwargs) -> str:
        return self.to_json(**kwargs)
