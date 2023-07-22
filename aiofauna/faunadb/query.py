from types import FunctionType


def abort(msg):
    return _fn({"abort": msg})


def ref(collection_ref, id=None):
    if id is None:
        return _fn({"@ref": collection_ref})
    return _fn({"ref": collection_ref, "id": id})


def collections(scope=None):
    return _fn({"collections": scope})


def documents(collections):
    return _fn({"documents": collections})


def databases(scope=None):
    return _fn({"databases": scope})


def indexes(scope=None):
    return _fn({"indexes": scope})


def functions(scope=None):
    return _fn({"functions": scope})


def roles(scope=None):
    return _fn({"roles": scope})


def access_providers(scope=None):
    return _fn({"access_providers": scope})


def keys(scope=None):
    return _fn({"keys": scope})


def tokens(scope=None):
    return _fn({"tokens": scope})


def credentials(scope=None):
    return _fn({"credentials": scope})


def at(timestamp, expr):
    return _fn({"at": timestamp, "expr": expr})


class LetBindings:
    def __init__(self, bindings):
        self._bindings = bindings

    def in_(self, inExpr):
        return _fn({"let": self._bindings, "in": inExpr})


def let(*args, **kwargs):
    if kwargs:
        return LetBindings([_fn({k: v}) for (k, v) in kwargs.items()])
    else:
        bindings = [_fn({k: v}) for (k, v) in args[0].items()]
        inExpr = args[1]
        return _fn({"let": bindings, "in": inExpr})


def var(var_name):
    return _fn({"var": var_name})


def if_(condition, then, else_):
    return _fn({"if": condition, "then": then, "else": else_})


def do(*expressions):
    return _fn({"do": expressions})


def lambda_query(func):
    vars = func.__code__.co_varnames
    n_args = len(vars)
    if n_args == 0:
        raise ValueError("Function must take at least 1 argument.")
    elif n_args == 1:
        v = vars[0]
        return lambda_(v, func(var(v)))
    else:
        return lambda_(vars, func(*[var(v) for v in vars]))


def lambda_(var_name_or_pattern, expr):
    return _fn({"lambda": var_name_or_pattern, "expr": expr})


def call(ref_, *arguments):
    return _fn({"call": ref_, "arguments": _varargs(arguments)})


def query(_lambda):
    if isinstance(_lambda, FunctionType):
        _lambda = lambda_query(_lambda)
    return _fn({"query": _lambda})


def map_(expr, collection):
    return _fn({"map": expr, "collection": collection})


def foreach(expr, collection):
    return _fn({"foreach": expr, "collection": collection})


def filter_(expr, collection):
    return _fn({"filter": expr, "collection": collection})


def take(number, collection):
    return _fn({"take": number, "collection": collection})


def drop(number, collection):
    return _fn({"drop": number, "collection": collection})


def prepend(elements, collection):
    return _fn({"prepend": elements, "collection": collection})


def append(elements, collection):
    return _fn({"append": elements, "collection": collection})


def is_empty(collection):
    return _fn({"is_empty": collection})


def is_nonempty(collection):
    return _fn({"is_nonempty": collection})


def is_number(expr):
    return _fn({"is_number": expr})


def is_double(expr):
    return _fn({"is_double": expr})


def is_integer(expr):
    return _fn({"is_integer": expr})


def is_boolean(expr):
    return _fn({"is_boolean": expr})


def is_null(expr):
    return _fn({"is_null": expr})


def is_bytes(expr):
    return _fn({"is_bytes": expr})


def is_timestamp(expr):
    return _fn({"is_timestamp": expr})


def is_date(expr):
    return _fn({"is_date": expr})


def is_string(expr):
    return _fn({"is_string": expr})


def is_array(expr):
    return _fn({"is_array": expr})


def is_object(expr):
    return _fn({"is_object": expr})


def is_ref(expr):
    return _fn({"is_ref": expr})


def is_set(expr):
    return _fn({"is_set": expr})


def is_doc(expr):
    return _fn({"is_doc": expr})


def is_lambda(expr):
    return _fn({"is_lambda": expr})


def is_collection(expr):
    return _fn({"is_collection": expr})


def is_database(expr):
    return _fn({"is_database": expr})


def is_index(expr):
    return _fn({"is_index": expr})


def is_function(expr):
    return _fn({"is_function": expr})


def is_key(expr):
    return _fn({"is_key": expr})


def is_token(expr):
    return _fn({"is_token": expr})


def is_credentials(expr):
    return _fn({"is_credentials": expr})


def is_role(expr):
    return _fn({"is_role": expr})


def get(ref_, ts=None):
    return _params({"get": ref_}, {"ts": ts})


def key_from_secret(secret):
    return _fn({"key_from_secret": secret})


def paginate(
    set, size=None, ts=None, after=None, before=None, events=None, sources=None
):
    opts = {
        "size": size,
        "ts": ts,
        "after": after,
        "before": before,
        "events": events,
        "sources": sources,
    }
    return _params({"paginate": set}, opts)


def exists(ref_, ts=None):
    return _params({"exists": ref_}, {"ts": ts})


def create(collection_ref, params):
    return _fn({"create": collection_ref, "params": params})


def update(ref_, params):
    return _fn({"update": ref_, "params": params})


def replace(ref_, params):
    return _fn({"replace": ref_, "params": params})


def delete(ref_):
    return _fn({"delete": ref_})


def insert(ref_, ts, action, params):
    return _fn({"insert": ref_, "ts": ts, "action": action, "params": params})


def remove(ref_, ts, action):
    return _fn({"remove": ref_, "ts": ts, "action": action})


def create_collection(collection_params):
    return _fn({"create_collection": collection_params})


def create_database(db_params):
    return _fn({"create_database": db_params})


def create_index(index_params):
    return _fn({"create_index": index_params})


def create_function(func_params):
    return _fn({"create_function": func_params})


def create_role(func_params):
    return _fn({"create_role": func_params})


def create_access_provider(provider_params):
    return _fn({"create_access_provider": provider_params})


def move_database(from_, to):
    return _fn({"move_database": from_, "to": to})


def create_key(key_params):
    return _fn({"create_key": key_params})


def singleton(ref_):
    return _fn({"singleton": ref_})


def events(ref_set):
    return _fn({"events": ref_set})


def match(index, *terms):
    m = {"match": index}
    if len(terms) >= 1:
        m["terms"] = _varargs(terms)
    return _fn(m)


def reverse(set_array_or_page):
    return _fn({"reverse": set_array_or_page})


def merge(merge, with_, lambda_=None):
    return _params({"merge": merge, "with": with_}, {"lambda": lambda_})


def union(*sets):
    return _fn({"union": _varargs(sets)})


def reduce(lambda_, initial, collection):
    return _fn({"reduce": lambda_, "initial": initial, "collection": collection})


def intersection(*sets):
    return _fn({"intersection": _varargs(sets)})


def difference(*sets):
    return _fn({"difference": _varargs(sets)})


def distinct(set):
    return _fn({"distinct": set})


def join(source, target):
    return _fn({"join": source, "with": target})


def range(set, from_, to):
    return _fn({"range": set, "from": from_, "to": to})


def login(ref_, params):
    return _fn({"login": ref_, "params": params})


def logout(delete_tokens):
    return _fn({"logout": delete_tokens})


def identify(ref_, password):
    return _fn({"identify": ref_, "password": password})


def current_identity():
    return _fn({"current_identity": None})


def has_current_identity():
    return _fn({"has_current_identity": None})


def current_token():
    return _fn({"current_token": None})


def has_current_token():
    return _fn({"has_current_token": None})


def has_identity():
    return _fn({"has_identity": None})


def format(string, *values):
    return _fn({"format": string, "values": _varargs(values)})


def concat(strings, separator=None):
    return _params({"concat": strings}, {"separator": separator})


def casefold(string, normalizer=None):
    return _params({"casefold": string}, {"normalizer": normalizer})


def starts_with(value, search):
    return _fn({"startswith": value, "search": search})


def ends_with(value, search):
    return _fn({"endswith": value, "search": search})


def contains_str(value, search):
    return _fn({"containsstr": value, "search": search})


def contains_str_regex(value, pattern):
    return _fn({"containsstrregex": value, "pattern": pattern})


def regex_escape(value):
    return _fn({"regexescape": value})


def ngram(terms, min=None, max=None):
    return _params({"ngram": terms}, {"min": min, "max": max})


def find_str(value, find, start=None):
    return _params({"findstr": value, "find": find}, {"start": start})


def find_str_regex(value, pattern, start=None, numResults=None):
    return _params(
        {"findstrregex": value, "pattern": pattern},
        {"start": start, "num_results": numResults},
    )


def replace_str(value, find, replace):
    return _fn({"replacestr": value, "find": find, "replace": replace})


def replace_str_regex(value, pattern, replace, first=None):
    return _params(
        {"replacestrregex": value, "pattern": pattern, "replace": replace},
        {"first": first},
    )


def length(value):
    return _fn({"length": value})


def lowercase(value):
    return _fn({"lowercase": value})


def uppercase(value):
    return _fn({"uppercase": value})


def titlecase(value):
    return _fn({"titlecase": value})


def trim(value):
    return _fn({"trim": value})


def ltrim(value):
    return _fn({"ltrim": value})


def rtrim(value):
    return _fn({"rtrim": value})


def space(count):
    return _fn({"space": count})


def substring(value, start, length=None):
    return _params({"substring": value, "start": start}, {"length": length})


def repeat(value, number=None):
    return _params({"repeat": value}, {"number": number})


def time(string):
    return _fn({"time": string})


def epoch(number, unit):
    return _fn({"epoch": number, "unit": unit})


def now():
    return _fn({"now": None})


def date(string):
    return _fn({"date": string})


def time_add(base, offset, unit):
    return _fn({"time_add": base, "offset": offset, "unit": unit})


def time_subtract(base, offset, unit):
    return _fn({"time_subtract": base, "offset": offset, "unit": unit})


def time_diff(start, finish, unit):
    return _fn({"time_diff": start, "other": finish, "unit": unit})


def new_id():
    return _fn({"new_id": None})


def database(db_name, scope=None):
    return _params({"database": db_name}, {"scope": scope})


def index(index_name, scope=None):
    return _params({"index": index_name}, {"scope": scope})


def collection(collection_name, scope=None):
    return _params({"collection": collection_name}, {"scope": scope})


def function(fn_name, scope=None):
    return _params({"function": fn_name}, {"scope": scope})


def role(role_name, scope=None):
    return _params({"role": role_name}, {"scope": scope})


def access_provider(access_provider_name, scope=None):
    return _params({"access_provider": access_provider_name}, {"scope": scope})


def equals(*values):
    return _fn({"equals": _varargs(values)})


def contains_path(path, in_):
    return _fn({"contains_path": path, "in": in_})


def contains_field(field, in_):
    return _fn({"contains_field": field, "in": in_})


def contains_value(value, in_):
    return _fn({"contains_value": value, "in": in_})


_NO_DEFAULT = object()


def select(path, from_, default=_NO_DEFAULT):
    _dict = {"select": path, "from": from_}
    if default is not _NO_DEFAULT:
        _dict["default"] = default
    return _fn(_dict)


def select_all(path, from_):
    return _fn({"select_all": path, "from": from_})


def add(*numbers):
    return _fn({"add": _varargs(numbers)})


def multiply(*numbers):
    return _fn({"multiply": _varargs(numbers)})


def subtract(*numbers):
    return _fn({"subtract": _varargs(numbers)})


def divide(*numbers):
    return _fn({"divide": _varargs(numbers)})


def pow(base, exp):
    return _fn({"pow": base, "exp": exp})


def max(*numbers):
    return _fn({"max": _varargs(numbers)})


def min(*numbers):
    return _fn({"min": _varargs(numbers)})


def abs(num):
    return _fn({"abs": num})


def trunc(num, precision=None):
    return _params({"trunc": num}, {"precision": precision})


def bitor(*numbers):
    return _fn({"bitor": _varargs(numbers)})


def cosh(num):
    return _fn({"cosh": num})


def hypot(num, b):
    return _fn({"hypot": num, "b": b})


def atan(num):
    return _fn({"atan": num})


def log(num):
    return _fn({"log": num})


def bitnot(*num):
    return _fn({"bitnot": _varargs(num)})


def bitxor(*num):
    return _fn({"bitxor": _varargs(num)})


def bitand(*num):
    return _fn({"bitand": _varargs(num)})


def ceil(num):
    return _fn({"ceil": num})


def degrees(num):
    return _fn({"degrees": num})


def cos(num):
    return _fn({"cos": num})


def acos(num):
    return _fn({"acos": num})


def sqrt(num):
    return _fn({"sqrt": num})


def tan(num):
    return _fn({"tan": num})


def tanh(num):
    return _fn({"tanh": num})


def sin(num):
    return _fn({"sin": num})


def asin(num):
    return _fn({"asin": num})


def round(num, precision=None):
    return _params({"round": num}, {"precision": precision})


def radians(num):
    return _fn({"radians": num})


def floor(num):
    return _fn({"floor": num})


def sign(num):
    return _fn({"sign": num})


def exp(num):
    return _fn({"exp": num})


def ln(num):
    return _fn({"ln": num})


def any(collection):
    return _fn({"any": collection})


def all(collection):
    return _fn({"all": collection})


def modulo(*numbers):
    return _fn({"modulo": _varargs(numbers)})


def count(collection):
    return _fn({"count": collection})


def sum(collection):
    return _fn({"sum": collection})


def mean(collection):
    return _fn({"mean": collection})


def lt(*values):
    return _fn({"lt": _varargs(values)})


def lte(*values):
    return _fn({"lte": _varargs(values)})


def gt(*values):
    return _fn({"gt": _varargs(values)})


def gte(*values):
    return _fn({"gte": _varargs(values)})


def and_(*booleans):
    return _fn({"and": _varargs(booleans)})


def or_(*booleans):
    return _fn({"or": _varargs(booleans)})


def not_(boolean):
    return _fn({"not": boolean})


def to_string(expr):
    return _fn({"to_string": expr})


def to_array(expr):
    return _fn({"to_array": expr})


def to_object(expr):
    return _fn({"to_object": expr})


def to_double(expr):
    return _fn({"to_double": expr})


def to_integer(expr):
    return _fn({"to_integer": expr})


def to_number(expr):
    return _fn({"to_number": expr})


def to_time(expr):
    return _fn({"to_time": expr})


def to_seconds(expr):
    return _fn({"to_seconds": expr})


def to_millis(expr):
    return _fn({"to_millis": expr})


def to_micros(expr):
    return _fn({"to_micros": expr})


def day_of_month(expr):
    return _fn({"day_of_month": expr})


def day_of_week(expr):
    return _fn({"day_of_week": expr})


def day_of_year(expr):
    return _fn({"day_of_year": expr})


def year(expr):
    return _fn({"year": expr})


def month(expr):
    return _fn({"month": expr})


def hour(expr):
    return _fn({"hour": expr})


def minute(expr):
    return _fn({"minute": expr})


def second(expr):
    return _fn({"second": expr})


def to_date(expr):
    return _fn({"to_date": expr})


class Expr:
    def __init__(self, value):
        self.value = value

    def to_fauna_json(self):
        return self.value

    def __repr__(self):
        return "Expr(%s)" % repr(self.value)

    def __eq__(self, other):
        return isinstance(other, Expr) and self.value == other.value


def _wrap(value):
    if isinstance(value, Expr):
        return value
    elif isinstance(value, FunctionType):
        return lambda_query(value)
    elif isinstance(value, dict):
        return Expr({"object": _wrap_values(value)})
    elif isinstance(value, (list, tuple)):
        return Expr([_wrap(sub_value) for sub_value in value])
    return value


def _wrap_values(dct):
    return {key: _wrap(val) for (key, val) in dct.items()}


def _fn(dct):
    return Expr(_wrap_values(dct))


def _params(main_params, optional_params):
    for key, val in optional_params.items():
        if val is not None:
            main_params[key] = val
    return _fn(main_params)


def _varargs(values):
    return values[0] if len(values) == 1 else values
