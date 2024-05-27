from typing import List, Optional, Tuple

from rdkit.Chem import Mol, MolFromSmiles, MolToSmiles

from ..problem import InvalidSmiles, Problem
from .step import Step

__all__ = ["CheckValidSmiles"]


class CheckValidSmiles(Step):
    """Checks if the molecule can be converted to SMILES and back."""

    def __init__(self):
        super().__init__()

    def _run(self, mol: Mol) -> Tuple[Optional[Mol], List[Problem]]:
        errors = []

        smi = MolToSmiles(mol, True)
        check_mol = MolFromSmiles(smi)
        if check_mol is None:
            errors.append(InvalidSmiles())
            mol = None

        return mol, errors
