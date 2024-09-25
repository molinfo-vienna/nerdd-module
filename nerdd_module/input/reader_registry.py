from functools import lru_cache, partial
from typing import Callable, Iterator, List, Type

from ..util import call_with_mappings, class_decorator
from .reader import Reader

__all__ = ["ReaderRegistry", "register_reader"]


ReaderFactory = Callable[[dict], Reader]


# lru_cache makes the registry a singleton
@lru_cache(maxsize=1)
class ReaderRegistry:
    def __init__(self) -> None:
        self._factories: List[ReaderFactory] = []

    def register(self, ReaderClass: Type[Reader], *args: str, **kwargs: str):
        assert issubclass(ReaderClass, Reader)
        assert all([isinstance(arg, str) for arg in args])
        assert all(
            [isinstance(k, str) and isinstance(v, str) for k, v in kwargs.items()]
        )
        self._factories.append(
            partial(
                call_with_mappings,
                ReaderClass,
                args_mapping=args,
                kwargs_mapping=kwargs,
            )
        )

    def get_readers(self, **kwargs) -> Iterator[Reader]:
        for factory in self._factories:
            yield factory(kwargs)


@class_decorator
def register_reader(cls, *args, **kwargs):
    ReaderRegistry().register(cls, *args, **kwargs)
