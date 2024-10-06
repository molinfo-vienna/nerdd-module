from io import BytesIO, StringIO
from typing import Any, BinaryIO, Iterable, Iterator

from .reader import ExploreCallable, MoleculeEntry, Reader

__all__ = ["ListReader"]


class ListReader(Reader):
    def __init__(self) -> None:
        super().__init__()

    def read(self, input_iterable: Any, explore: ExploreCallable) -> Iterator[MoleculeEntry]:
        assert isinstance(input_iterable, Iterable) and not isinstance(
            input_iterable, (str, bytes, BytesIO, StringIO, BinaryIO)
        ), f"input must be an iterable, but is {type(input_iterable)}"

        for entry in input_iterable:
            yield from explore(entry)

    def __repr__(self) -> str:
        return "ListReader()"
