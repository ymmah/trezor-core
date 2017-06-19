from typing import Callable, Generator, Iterator, List, Union
import sys
import gc

from trezorutils import halt, memcpy


def _gf() -> Generator:
    yield


type_gen = type(_gf())


def _unimport_func(func):  # type: ignore
    def inner(*args, **kwargs):  # type: ignore
        mods = set(sys.modules)
        try:
            ret = func(*args, **kwargs)
        finally:
            for mod in sys.modules:
                if mod not in mods:
                    del sys.modules[mod]
            gc.collect()
        return ret
    return inner


def _unimport_gen(genfunc):  # type: ignore
    async def inner(*args, **kwargs):  # type: ignore
        mods = set(sys.modules)
        try:
            ret = await genfunc(*args, **kwargs)
        finally:
            for mod in sys.modules:
                if mod not in mods:
                    del sys.modules[mod]
            gc.collect()
        return ret
    return inner


def unimport(func):  # type: ignore
    if isinstance(func, type_gen):
        return _unimport_gen(func)  # type: ignore
    else:
        return _unimport_func(func)  # type: ignore


def chunks(items: List, size: int) -> Iterator[List]:
    for i in range(0, len(items), size):
        yield items[i:i + size]


def ensure(cond: bool) -> None:
    if not cond:
        raise AssertionError()
