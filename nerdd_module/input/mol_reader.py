from typing import Any, Iterator

from rdkit.Chem import Mol

from .reader import ExploreCallable, MoleculeEntry, Reader


class MolReader(Reader):
    def __init__(self) -> None:
        super().__init__()

    def read(self, mol: Any, explore: ExploreCallable) -> Iterator[MoleculeEntry]:
        assert isinstance(mol, Mol)
        yield MoleculeEntry(
            raw_input=mol,
            input_type="rdkit_mol",
            source=("raw_input",),
            mol=mol,
            errors=[],
        )

    def __repr__(self) -> str:
        return "MolReader()"
