from typing import List, Tuple

from rdkit.Chem import Mol
from rdkit.Chem import RemoveStereochemistry as remove_stereochemistry

from .step import Step


class RemoveStereochemistry(Step):
    def __init__(self):
        super().__init__()

    def _run(self, mol: Mol) -> Tuple[Mol, List[str]]:
        errors = []

        try:
            remove_stereochemistry(mol)
        except Exception as e:
            errors.append("!2")

        return mol, errors
