import collections
from typing import Union, Any, Iterable, Iterator, List

epsilon = 1e-4

def clamp(n, minn, maxn):
    if n < minn:
        return minn
    elif n > maxn:
        return maxn
    else:
        return n

def flatten(l: Iterable[Union[Any, Iterable[Any]]]) -> List[Any]:
    def gen():
        for el in l:
            if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
                yield from flatten(el)
            else:
                yield el

    return list(gen())

class MicroMock(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

