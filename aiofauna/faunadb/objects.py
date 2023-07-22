"""
Types used in queries and responses.
See the `docs <https://app.fauna.com/documentation/reference/queryapi#simple-type>`__.
"""
from datetime import datetime

from iso8601 import parse_date

from .query import Expr


class Ref(Expr):
    """
    ```python
    Ref(id, cls=None, db=None)
    ```
    A reference to a document in a collection or index.

    :param id: The document's ID.
    :param cls: The collection or index class.
    :param db: The database.

    `Ref`

    Is a special type in FaunaDB. It is used to represent a document in a collection or index.

    It is serialized to JSON as an object with the `@ref` key. Passing the `id` to the response.

    """

    def __init__(self, id, cls=None, db=None):
        if id is None:
            raise ValueError("The Ref must have an id.")

        value = {"id": id}

        if cls != None:
            value["collection"] = cls

        if db != None:
            value["database"] = db

        super(Ref, self).__init__(value)

    def collection(self):
        """
        Gets the collection part out of the Ref.
        """
        return self.value.get("collection")

    def database(self):
        """
        Gets the database part out of the Ref.
        """
        return self.value.get("database")

    def id(self):
        """
        Gets the id part out of the Ref.
        """
        return self.value["id"]

    def to_fauna_json(self):
        return {"@ref": self.value}

    def __str__(self):
        col = (
            f", collection={self.value['collection']}"
            if "collection" in self.value
            else ""
        )
        db = (
            f", database={self.value.get('database')}"
            if "database" in self.value
            else ""
        )
        return "Ref(id=%s%s%s)" % (self.value["id"], col, db)

    def __repr__(self):
        col = (
            f", collection={self.value['collection']}"
            if "collection" in self.value
            else ""
        )
        db = (
            f", database={self.value.get('database')}"
            if "database" in self.value
            else ""
        )
        return "Ref(id=%s%s%s)" % (self.value["id"], col, db)

    def __eq__(self, other):
        return isinstance(other, Ref) and self.value == other.value

    def __ne__(self, other):
        # pylint: disable=unneeded-not
        return not self == other


class Native(object):
    COLLECTIONS = Ref("collections")
    INDEXES = Ref("indexes")
    DATABASES = Ref("databases")
    FUNCTIONS = Ref("functions")
    KEYS = Ref("keys")
    TOKENS = Ref("tokens")
    CREDENTIALS = Ref("credentials")
    ROLES = Ref("roles")
    ACCESS_PROVIDERS = Ref("access_providers")

    def __init__(self):
        raise TypeError

    @classmethod
    def from_name(cls, name):
        return getattr(cls, name.upper(), Ref(name))


class SetRef(Expr):
    """
    FaunaDB Set.
    This represents a set returned as part of a response.
    For query sets see :doc:`query`.
    """

    def __init__(self, set_ref):
        if isinstance(set_ref, Expr):
            value = set_ref.value
        else:
            value = set_ref

        super(SetRef, self).__init__(value)

    def to_fauna_json(self):
        return {"@set": self.value}

    def __repr__(self):
        return f"SetRef({repr(self.value)})"

    def __eq__(self, other):
        return isinstance(other, SetRef) and self.value == other.value

    def __ne__(self, other):
        # pylint: disable=unneeded-not
        return not self == other


class FaunaTime(Expr):
    """
    FaunaDB time. See the `docs <https://app.fauna.com/documentation/reference/queryapi#special-type>`__.

    For dates, regular :class:`datetime.date` objects are used.
    """

    def __init__(self, value):
        """
        :param value:
          If a :class:`datetime.datetime` is passed, it is converted to a string.
          Must include an offset.
        """
        if isinstance(value, datetime):
            if value.utcoffset() is None:
                raise ValueError("FaunaTime requires offset-aware datetimes")
            value = value.isoformat()

        # Convert +00:00 offset to zulu for comparison equality
        # We don't check for +0000 or +00 as they are not valid in FaunaDB
        super(FaunaTime, self).__init__(value.replace("+00:00", "Z"))

    def to_datetime(self):
        """
        Convert to an offset-aware datetime object.
        This is lossy as datetimes have microsecond rather than nanosecond precision.
        """
        return parse_date(self.value)

    def to_fauna_json(self):
        return {"@ts": self.value}

    def __repr__(self):
        return "FaunaTime(%s)" % repr(self.value)

    def __eq__(self, other):
        return isinstance(other, FaunaTime) and self.value == other.value

    def __ne__(self, other):
        # pylint: disable=unneeded-not
        return not self == other


class Query(Expr):
    """
    Represents a `@query` type in FaunaDB.
    See the `docs <https://app.fauna.com/documentation/reference/queryapi#special-type>`__.
    """

    def to_fauna_json(self):
        return {"@query": self.value}

    def __repr__(self):
        return "Query(%s)" % repr(self.value)

    def __eq__(self, other):
        return isinstance(other, Query) and self.value == other.value

    def __ne__(self, other):
        # pylint: disable=unneeded-not
        return not self == other
