from io import BytesIO
from typing import Any, Iterator

from .reader import ExploreCallable, MoleculeEntry, Reader

__all__ = ["StringReader"]


class StringReader(Reader):
    def __init__(self) -> None:
        super().__init__()

    def read(self, input: Any, explore: ExploreCallable) -> Iterator[MoleculeEntry]:
        assert isinstance(input, (str, bytes))

        if isinstance(input, str):
            input = input.encode("utf-8")

        with BytesIO(input) as f:
            yield from explore(f)

    def __repr__(self) -> str:
        return "StringReader()"
