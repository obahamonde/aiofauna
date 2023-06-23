from . import query


class Page:
    @staticmethod
    def from_raw(raw):
        return Page(raw["data"], raw.get("before"), raw.get("after"))

    def __init__(self, data, before=None, after=None):
        self.data = data
        self.before = before
        self.after = after

    def map_data(self, func):
        return Page([func(x) for x in self.data], self.before, self.after)

    def __repr__(self):
        return "Page(data=%s, before=%s, after=%s)" % (
            self.data,
            self.before,
            self.after,
        )

    def __eq__(self, other):
        return (
            isinstance(other, Page)
            and self.data == other.data
            and self.before == other.before
            and self.after == other.after
        )

    @staticmethod
    def set_iterator(client, set_query, map_lambda=None, mapper=None, page_size=None):
        def get_page(**kwargs):
            queried = query.paginate(set_query, **kwargs)
            if map_lambda is not None:
                queried = query.map_(map_lambda, queried)
            return Page.from_raw(client.query(queried))

        page = get_page(size=page_size)
        for val in page.data:
            yield val if mapper is None else mapper(val)
        next_cursor = "after" if page.after is not None else "before"
        while getattr(page, next_cursor) is not None:
            page = get_page(
                **{"size": page_size, next_cursor: getattr(page, next_cursor)}
            )
            for val in page.data:
                yield val if mapper is None else mapper(val)
