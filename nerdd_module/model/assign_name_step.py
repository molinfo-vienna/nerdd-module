from typing import Iterable, Iterator, Union

from ..steps import MapStep

__all__ = ["AssignNameStep"]


class AssignNameStep(MapStep):
    def __init__(self) -> None:
        super().__init__()

    def _process(self, record: dict) -> Union[dict, Iterable[dict], Iterator[dict]]:
        mol = record.get("input_mol")

        record["name"] = mol.GetProp("_Name") if mol is not None and mol.HasProp("_Name") else ""

        return record
