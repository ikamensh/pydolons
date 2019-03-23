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
            if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
                yield from flatten(el)
            else:
                yield el

    return list(gen())

class ReadOnlyDict(dict):
    def __readonly__(self, *args, **kwargs):
        raise RuntimeError("Cannot modify ReadOnlyDict")
    __setitem__ = __readonly__
    __delitem__ = __readonly__
    pop = __readonly__
    popitem = __readonly__
    clear = __readonly__
    update = __readonly__
    setdefault = __readonly__
    del __readonly__

