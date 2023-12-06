import os
from abc import ABC, abstractmethod
from typing import BinaryIO, Generator

from .elementary_reader import ElementaryReader
from .reader import MoleculeEntry, Reader

__all__ = ["FileReader"]


class FileReader(Reader):
    def __init__(self, elementary_reader: ElementaryReader):
        super().__init__()
        self._elementary_reader = elementary_reader

    def read(self, input) -> Generator[MoleculeEntry, None, None]:
        if not isinstance(input, str) or not os.path.exists(input):
            raise TypeError("input must be a valid filename")

        with open(input, "rb") as f:
            for block in self._split(f):
                for entry in self._elementary_reader.read(block):
                    yield entry._replace(source=input)

    @abstractmethod
    def _split(self, f: BinaryIO) -> Generator[str, None, None]:
        pass

    def _input_type(self) -> str:
        return self._elementary_reader.input_type
