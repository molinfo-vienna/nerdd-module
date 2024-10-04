from typing import Iterable

from .writer import Writer

__all__ = ["IteratorWriter"]


class IteratorWriter(Writer, output_format="iterator"):
    def __init__(self) -> None:
        pass

    def write(self, records: Iterable[dict]) -> Iterable[dict]:
        return records
