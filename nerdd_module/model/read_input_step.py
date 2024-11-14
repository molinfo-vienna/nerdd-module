from typing import Any, Iterator

from ..input.explorer import Explorer
from ..steps import Step

__all__ = ["ReadInputStep"]


class ReadInputStep(Step):
    def __init__(self, explorer: Explorer, input: Any) -> None:
        super().__init__(is_source=True)
        self._explorer = explorer
        self._input = input

    def _run(self, source: Iterator[dict]) -> Iterator[dict]:
        for entry in self._explorer.explore(self._input):
            record = dict(
                input_text=entry.raw_input,
                source=entry.source,
                input_type=entry.input_type,
                input_mol=entry.mol,
                problems=entry.errors,
            )
            yield record
