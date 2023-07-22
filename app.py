import math
import typing
from functools import wraps
from json import dumps, loads
from pathlib import Path
from threading import Lock

T = typing.TypeVar("T")  

def tree_to_json(path:str=".")->dict:
    path_ = Path(path)
    if not path_.exists():
        raise FileNotFoundError(f"{path} does not exist")
    if path_.is_file():
        try:
            return path_.read_text()
        except:
            return "[binary]"
    else:
        return {i.name:tree_to_json(i) for i in path_.iterdir()}
    
    
def get_tree(path:str=".")->str:
    path_ = Path(path)
    if not path_.exists():
        raise FileNotFoundError(f"{path} does not exist")
    if path_.is_file():
        try:
            return path_.read_text()
        except:
            return "[binary]"
    else:
        dct = {i.name:tree_to_json(i) for i in path_.iterdir()}
        for k, v in dct.items():
            if isinstance(v, dict):
                text = f"{k}\n" + "\n".join([f"├── {i}" for i in v.keys()])
            else:
                text = f"{k}\n" + "\n".join([f"├── {i}" for i in v.split("\n")])        
            dct[k] = text
        return "\n".join([f"├── {i}" for i in dct.keys()]) + "\n" + "\n".join(dct.values())

def token_estimate(text:str):
    byte_size = len(text.encode('utf-8'))
    return math.ceil(byte_size / 4)


def divide_in_chunks_for_openai_api(text:str, max_tokens:int=1024):
    tokens = token_estimate(text)
    if tokens <= max_tokens:
        return [text]
    else:
        return [text[i:i+max_tokens] for i in range(0, len(text), max_tokens)]
    
  

def singleton(cls: typing.Type[T]) -> typing.Callable[..., T]:
    instance = None
    lock = Lock()
    
    @wraps(cls)
    def wrapper(*args, **kwargs):
        nonlocal instance
        if instance is None:
            with lock:
                if instance is None:
                    instance = cls(*args, **kwargs)
        return instance
    return wrapper

