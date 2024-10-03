from typing import Iterable

from .writer import Writer

__all__ = ["IteratorWriter"]


class IteratorWriter(Writer):
    def __init__(self) -> None:
        pass

    def write(self, records: Iterable[dict]) -> Iterable[dict]:
        return records

    @classmethod
    def get_output_format(cls) -> str:
        return "iterator"
