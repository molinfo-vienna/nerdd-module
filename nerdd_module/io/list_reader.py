from typing import Generator, Iterable

from .reader import MoleculeEntry, Reader

__all__ = ["ListReader"]


class ListReader(Reader):
    def __init__(self, inner_reader: Reader):
        super().__init__()
        self._inner_reader = inner_reader

    def read(self, input) -> Generator[MoleculeEntry, None, None]:
        if not isinstance(input, Iterable) or isinstance(input, str):
            raise TypeError("input must be iterable")

        for item in input:
            for entry in self._inner_reader.read(item):
                yield entry

    def _input_type(self) -> str:
        return self._inner_reader.input_type
