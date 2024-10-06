from typing import List, Tuple

from rdkit.Chem import Mol
from rdkit.Chem import RemoveStereochemistry as remove_stereochemistry

from ..problem import Problem
from .preprocessing_step import PreprocessingStep


class RemoveStereochemistry(PreprocessingStep):
    def __init__(self) -> None:
        super().__init__()

    def _preprocess(self, mol: Mol) -> Tuple[Mol, List[Problem]]:
        problems = []

        try:
            remove_stereochemistry(mol)
        except Exception:
            problems.append(
                Problem("remove_stereochemistry_failed", "Cannot remove stereochemistry")
            )

        return mol, problems
