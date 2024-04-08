from functools import lru_cache
from typing import Dict, Generator, List, Tuple, Type

from .reader import Reader

__all__ = ["ReaderRegistry", "register_reader"]


# lru_cache makes the registry a singleton
@lru_cache(maxsize=1)
class ReaderRegistry:
    def __init__(self):
        self._factories : List[Tuple[Type[Reader], Tuple[str, ...], Dict[str, str]]] = []
        self._config = {}

    def _create_reader(self, ReaderClass: Type[Reader], *args, **kwargs) -> Reader:
        # translate all args
        args = [self._config.get(arg, None) for arg in args]
        # translate all kwargs
        kwargs = {k: self._config.get(v, None) for k, v in kwargs.items() if v in self._config}

        return ReaderClass(*args, **kwargs)

    def register(self, ReaderClass: Type[Reader], *args :str , **kwargs:str):
        assert issubclass(ReaderClass, Reader)
        assert all([isinstance(arg, str) for arg in args])
        assert all([isinstance(k, str) and isinstance(v, str) for k, v in kwargs.items()])
        self._factories.append((ReaderClass, args, kwargs))

    def readers(self) -> Generator[Reader, None, None]:
        for reader, args, kwargs in self._factories:
            yield self._create_reader(reader, *args, **kwargs)

    def __iter__(self):
        return iter(self.readers())


def register_reader(*args, **kwargs):
    def wrapper(cls, *args, **kwargs):
        ReaderRegistry().register(cls, *args, **kwargs)
        return cls

    # Case 1: first argument is a class 
    # --> decorator is used without arguments 
    # @register_reader
    # class F:
    #     ...
    if len(args) > 0 and isinstance(args[0], type):
        return wrapper(args[0], *args[1:], **kwargs)
    
    # Case 2: first argument is a not a class
    # --> decorator is used with arguments
    # @register_reader("blah")
    # class F:
    #     ...
    def inner(cls):
        assert isinstance(cls, type), "Decorator must be used with a class"
        return wrapper(cls, *args, **kwargs)
    return inner
