from __future__ import annotations

import codecs
import inspect
from abc import ABC, ABCMeta, abstractmethod
from functools import partial
from typing import Any, Callable, Dict, Iterable, List, Type

from ..util import call_with_mappings

StreamWriter = codecs.getwriter("utf-8")

__all__ = ["Writer"]

_factories: Dict[str, Callable[[dict], Writer]] = {}


class WriterMeta(ABCMeta):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)

        if not inspect.isabstract(cls):
            output_format = cls.get_output_format()
            _factories[output_format] = partial(call_with_mappings, cls)


class Writer(ABC, metaclass=WriterMeta):
    """Abstract class for writers."""

    def __init__(self):
        pass

    @abstractmethod
    def write(self, records: Iterable[dict]) -> Any:
        pass

    @classmethod
    def get_writer(cls, output_format: str, **kwargs) -> Writer:
        if output_format not in _factories:
            raise ValueError(f"Unknown output format: {output_format}")
        return _factories[output_format](kwargs)

    @classmethod
    def get_output_formats(self) -> List[str]:
        return list(_factories.keys())
