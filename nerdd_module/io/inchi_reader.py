from typing import Iterable, Optional, Tuple

from rdkit import RDLogger
from rdkit.Chem import Mol, MolFromInchi

from .elementary_reader import ElementaryReader

__all__ = ["InchiReader"]


class InchiReader(ElementaryReader):
    def __init__(self):
        super().__init__()

    def _read(self, input) -> Tuple[Optional[Mol], Iterable[str]]:
        if not isinstance(input, str):
            raise TypeError("input must be a string")

        # suppress RDKit warnings
        lg = RDLogger.logger()
        lg.setLevel(RDLogger.CRITICAL)

        mol = MolFromInchi(input)

        if mol is None:
            errors = ["!1"]
        else:
            errors = []

        lg.setLevel(RDLogger.WARNING)

        return mol, errors

    def _input_type(self) -> str:
        return "inchi"
