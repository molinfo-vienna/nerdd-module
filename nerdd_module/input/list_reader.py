from io import BytesIO, StringIO
from typing import BinaryIO, Generator, Iterable

from .reader import MoleculeEntry, Reader
from .reader_registry import register_reader

__all__ = ["ListReader"]


@register_reader
class ListReader(Reader):
    def __init__(self):
        super().__init__()

    def read(self, input_iterable, explore) -> Generator[MoleculeEntry, None, None]:
        assert isinstance(input_iterable, Iterable) and not isinstance(
            input_iterable, (str, bytes, BytesIO, StringIO, BinaryIO)
        ), f"input must be an iterable, but is {type(input_iterable)}"

        for entry in input_iterable:
            yield from explore(entry)

    def __repr__(self) -> str:
        return "ListReader()"
