from typing import Iterator

from ..steps import Step

__all__ = ["AssignMolIdStep"]


class AssignMolIdStep(Step):
    def __init__(self) -> None:
        super().__init__()

    def _run(self, source: Iterator[dict]) -> Iterator[dict]:
        mol_id = 0
        for record in source:
            record["mol_id"] = mol_id
            mol_id += 1
            yield record
