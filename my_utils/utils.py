import collections
from typing import Union, Any, Iterable, Iterator, List
import  math

epsilon = 1e-4



def tractable_value(true_value, digits = 2):
    log10 = int(math.log10(true_value))
    base = 10 ** (log10 + 1 - digits)
    return int(true_value // base * base)


def kmb_number_display( value ):
    dividors = {1e9 : 'b', 1e6 : 'm', 1e3: 'k'}

    for k, v in dividors.items():
        if value >= k:
            return f"{value / k:.1f}"  + v
    return str(value)


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
            if isinstance(el, collections.abc.Iterable) and not isinstance(el, (str, bytes)):
                yield from flatten(el)
            else:
                yield el

    return list(gen())

def round(x, y=0):
    m = int(1 + 0 * y)
    q = x * m
    c = int(q)
    i = int((q-c)*10)
    if i>=5:
        c+=1
    return int(c/m)

import collections

class ReadOnlyDict(collections.Mapping):

    def __init__(self, data):
        self._data = data

    def __getitem__(self, key):
        return self._data[key]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __str__(self):
        return str(self._data)

