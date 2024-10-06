from __future__ import annotations

import codecs
from abc import ABC, abstractmethod
from functools import partial
from typing import Any, Dict, Iterable, List, Optional

from typing_extensions import Protocol

from ..util import call_with_mappings

StreamWriter = codecs.getwriter("utf-8")

__all__ = ["Writer"]


class WriterFactory(Protocol):
    def __call__(self, config: dict, *args: Any, **kwargs: Any) -> Writer: ...


_factories: Dict[str, WriterFactory] = {}


class Writer(ABC):
    """Abstract class for writers."""

    def __init__(self) -> None:
        pass

    @classmethod
    def __init_subclass__(
        cls,
        output_format: Optional[str] = None,
        is_abstract: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init_subclass__(**kwargs)
        if not is_abstract:
            assert output_format is not None, "output_format must not be None"
            _factories[output_format] = partial(call_with_mappings, cls)

    @abstractmethod
    def write(self, records: Iterable[dict]) -> Any:
        pass

    @classmethod
    def get_writer(cls, output_format: str, **kwargs: Any) -> Writer:
        if output_format not in _factories:
            raise ValueError(f"Unknown output format: {output_format}")
        return _factories[output_format](kwargs)

    @classmethod
    def get_output_formats(self) -> List[str]:
        return list(_factories.keys())
