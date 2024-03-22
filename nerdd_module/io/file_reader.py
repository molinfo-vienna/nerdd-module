import os
from typing import Generator

from .reader import MoleculeEntry, Reader
from .reader_registry import register_reader

__all__ = ["FileReader"]


@register_reader
class FileReader(Reader):
    def __init__(self):
        super().__init__()

    def read(self, filename, explore) -> Generator[MoleculeEntry, None, None]:
        if not isinstance(filename, str) or not os.path.exists(filename):
            raise TypeError("input must be a valid filename")

        with open(filename, "rb") as f:
            for entry in explore(f):
                if len(entry.source) == 1 and entry.source[0] == "raw_input":
                    source = tuple()
                else:
                    source = entry.source
                yield entry._replace(source=tuple([filename, *source]))

    def __repr__(self):
        return f"FileReader()"
