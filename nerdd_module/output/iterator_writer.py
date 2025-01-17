from typing import Iterable

from .writer import Writer
from .writer_config import WriterConfig

__all__ = ["IteratorWriter"]


class IteratorWriter(Writer):
    def __init__(self) -> None:
        pass

    def write(self, records: Iterable[dict]) -> Iterable[dict]:
        return records

    config = WriterConfig(output_format="iterator")
