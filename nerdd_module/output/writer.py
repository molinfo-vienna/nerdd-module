import codecs
from abc import ABC, abstractmethod
from typing import Any, Iterable

StreamWriter = codecs.getwriter("utf-8")

__all__ = ["Writer"]


class Writer(ABC):
    """Abstract class for writers."""

    def __init__(self):
        pass

    @abstractmethod
    def write(self, records: Iterable[dict]) -> Any:
        pass
