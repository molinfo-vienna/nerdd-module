from functools import lru_cache
from typing import Generator, Type

from .reader import Reader

__all__ = ["ReaderRegistry", "register_reader"]


# lru_cache makes the registry a singleton
@lru_cache(maxsize=1)
class ReaderRegistry:
    def __init__(self):
        self._factories = []

    def register(self, ReaderClass: Type[Reader], *args, **kwargs):
        assert issubclass(ReaderClass, Reader)
        self._factories.append(lambda: ReaderClass(*args, **kwargs))

    def readers(self) -> Generator[Reader, None, None]:
        for reader in self._factories:
            yield reader()

    def __iter__(self):
        return iter(map(lambda f: f(), self._factories))


def register_reader(clazz, *args, **kwargs):
    # TODO: implement both decorator modes
    ReaderRegistry().register(clazz, *args, **kwargs)
    return clazz
