from typing import BinaryIO, Generator, Iterable, List, Optional, Tuple

from rdkit import RDLogger
from rdkit.Chem import Mol, MolFromMolBlock

from .elementary_reader import ElementaryReader

__all__ = ["MolBlockReader"]


class MolBlockReader(ElementaryReader):
    def __init__(self):
        super().__init__()

    def _read(self, input) -> Tuple[Optional[Mol], Iterable[str]]:
        if not isinstance(input, str):
            raise TypeError("input must be a string")

        # suppress RDKit warnings
        lg = RDLogger.logger()
        lg.setLevel(RDLogger.CRITICAL)

        # MolFromMolBlock never raises an exception
        # it returns None if the mol block is invalid
        mol = MolFromMolBlock(input)

        if mol is None:
            errors = ["!1"]
        else:
            errors = []

        lg.setLevel(RDLogger.WARNING)

        return mol, errors

    def _input_type(self) -> str:
        return "mol_block"
