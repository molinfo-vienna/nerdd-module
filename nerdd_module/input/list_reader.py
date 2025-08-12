from io import IOBase
from typing import Any, Iterable, Iterator

from ..problem import Problem
from .reader import ExploreCallable, MoleculeEntry, Reader

__all__ = ["ListReader"]


class ListReader(Reader):
    def __init__(self) -> None:
        super().__init__()

    def read(self, input_iterable: Any, explore: ExploreCallable) -> Iterator[MoleculeEntry]:
        assert isinstance(input_iterable, Iterable) and not isinstance(
            input_iterable, (str, bytes, IOBase)
        ), f"input must be an iterable, but is {type(input_iterable)}"

        for entry in input_iterable:
            try:
                yield from explore(entry)
            except Exception as e:
                raw_input = str(entry)
                if len(raw_input) > 100:
                    raw_input = raw_input[:97] + "..."
                yield MoleculeEntry(
                    raw_input=raw_input,
                    input_type="unknown",
                    source=(),
                    mol=None,
                    errors=[Problem("invalid_list_entry", f"Could not read list entry: {e}")],
                )

    def __repr__(self) -> str:
        return "ListReader()"
