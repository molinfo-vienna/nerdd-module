from functools import lru_cache, partial
from typing import Callable, Dict, Type

from ..util import call_with_mappings, class_decorator
from .writer import Writer

__all__ = [
    "WriterRegistry",
    "register_writer",
]


WriterFactory = Callable[[dict], Writer]


# lru_cache makes the registry a singleton
@lru_cache(maxsize=1)
class WriterRegistry:
    def __init__(self) -> None:
        self._factories: Dict[str, WriterFactory] = {}

    def register(
        self,
        output_format: str,
        WriterClass: Type[Writer],
        *args: str,
        **kwargs: str,
    ):
        assert issubclass(WriterClass, Writer)
        assert all([isinstance(arg, str) for arg in args])
        assert all(
            [isinstance(k, str) and isinstance(v, str) for k, v in kwargs.items()]
        )

        self._factories[output_format] = partial(
            call_with_mappings, WriterClass, args_mapping=args, kwargs_mapping=kwargs
        )

    def get_writer(self, output_format: str, **kwargs) -> Writer:
        if output_format not in self._factories:
            raise ValueError(f"Unknown output format: {output_format}")
        return self._factories[output_format](kwargs)

    def get_output_formats(self) -> frozenset:
        return frozenset(self._factories.keys())


@class_decorator
def register_writer(cls: Type[Writer], output_format: str, *args, **kwargs):
    WriterRegistry().register(output_format, cls, *args, **kwargs)
