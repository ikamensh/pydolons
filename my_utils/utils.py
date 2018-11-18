import collections
from typing import Union, Any, Iterable, Iterator, List
import  math

epsilon = 1e-4

def tractable_value(true_value, digits = 2):
    log10 = int(math.log10(true_value))
    base = 10 ** (log10 + 1 - digits)
    return int(true_value // base * base)

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

