from typing import List, Tuple

from rdkit.Chem import Mol
from rdkit.Chem import RemoveStereochemistry as remove_stereochemistry

from ..problem import Problem
from .step import Step


class RemoveStereochemistry(Step):
    def __init__(self):
        super().__init__()

    def _run(self, mol: Mol) -> Tuple[Mol, List[Problem]]:
        errors = []

        try:
            remove_stereochemistry(mol)
        except Exception:
            errors.append(
                Problem("remove_stereochemistry", "Cannot remove stereochemistry")
            )

        return mol, errors
