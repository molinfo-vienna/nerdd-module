from typing import Iterable, Optional, Tuple

from rdkit import RDLogger
from rdkit.Chem import Mol, MolFromSmiles

from .elementary_reader import ElementaryReader

__all__ = ["SmilesReader"]


class SmilesReader(ElementaryReader):
    def __init__(self):
        super().__init__()

    def _read(self, input) -> Tuple[Optional[Mol], Iterable[str]]:
        if not isinstance(input, str):
            raise TypeError("input must be a string")

        # suppress RDKit warnings
        lg = RDLogger.logger()
        lg.setLevel(RDLogger.CRITICAL)

        mol = MolFromSmiles(input)

        lg.setLevel(RDLogger.WARNING)

        if mol is None:
            return None, ["!1"]

        # old versions of RDKit do not parse the name
        # --> get name from smiles manually
        if not mol.HasProp("_Name"):
            parts = input.split(maxsplit=1)
            if len(parts) > 1:
                mol.SetProp("_Name", parts[1])

        return mol, []

    def _input_type(self) -> str:
        return "smiles"
