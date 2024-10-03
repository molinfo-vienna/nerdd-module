from typing import List, Optional, Tuple

from rdkit.Chem import Mol, MolFromSmiles, MolToSmiles

from ..problem import InvalidSmiles, Problem
from .preprocessing_step import PreprocessingStep

__all__ = ["CheckValidSmiles"]


class CheckValidSmiles(PreprocessingStep):
    """Checks if the molecule can be converted to SMILES and back."""

    def __init__(self) -> None:
        super().__init__()

    def _preprocess(self, mol: Mol) -> Tuple[Optional[Mol], List[Problem]]:
        problems = []

        smi = MolToSmiles(mol, True)
        check_mol = MolFromSmiles(smi)
        if check_mol is None:
            problems.append(InvalidSmiles())
            mol = None

        return mol, problems
