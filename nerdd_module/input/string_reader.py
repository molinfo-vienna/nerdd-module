from io import BytesIO
from typing import Generator

from .reader import MoleculeEntry, Reader
from .reader_registry import register_reader

__all__ = ["StringReader"]


@register_reader
class StringReader(Reader):
    def __init__(self):
        super().__init__()

    def read(self, input, explore) -> Generator[MoleculeEntry, None, None]:
        assert isinstance(input, str)

        with BytesIO(input.encode("utf-8")) as f:
            yield from explore(f)

    def __repr__(self) -> str:
        return "StringReader()"
