from typing import Iterable, Iterator, Union

from rdkit.Chem import MolToSmiles

from ..steps import MapStep

__all__ = ["AddSmilesStep"]


class AddSmilesStep(MapStep):
    def __init__(self, mol_column: str, smiles_column: str) -> None:
        super().__init__()
        self._mol_column = mol_column
        self._smiles_column = smiles_column

    def _process(self, record: dict) -> Union[dict, Iterable[dict], Iterator[dict]]:
        mol = record[self._mol_column]

        try:
            smiles = MolToSmiles(mol)
        except:  # noqa: E722 (allow bare except, because RDKit is unpredictable)
            smiles = None

        record[self._smiles_column] = smiles
        return record
