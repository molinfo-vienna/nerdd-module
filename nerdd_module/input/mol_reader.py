from typing import Generator

from rdkit.Chem import Mol

from .reader import MoleculeEntry, Reader
from .reader_registry import register_reader


@register_reader
class MolReader(Reader):
    def __init__(self):
        super().__init__()

    def read(self, mol, explore) -> Generator[MoleculeEntry, None, None]:
        assert isinstance(mol, Mol)
        yield MoleculeEntry(
            raw_input=mol,
            input_type="rdkit_mol",
            source=tuple(["raw_input"]),
            mol=mol,
            errors=[],
        )

    def __repr__(self) -> str:
        return "MolReader()"
