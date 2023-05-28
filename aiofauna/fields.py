from pydantic.fields import \
    Field as PydanticField  # pylint: disable=no-name-in-module


def Field(*args, index:bool=False, unique:bool=False, **kwargs):
    """Field Factory"""
    return PydanticField(*args, index=index, unique=unique, **kwargs)