from typing import List, Tuple

from rdkit.Chem import Mol, MolFromSmiles, MolToSmiles

from ..problem import Problem
from .step import Step

__all__ = ["CheckValidSmiles"]


class CheckValidSmiles(Step):
    """Checks if the molecule can be converted to SMILES and back."""

    def __init__(self):
        super().__init__()

    def _run(self, mol: Mol) -> Tuple[Mol, List[Problem]]:
        errors = []

        smi = MolToSmiles(mol, True)
        check_mol = MolFromSmiles(smi)
        if check_mol is None:
            errors.append(
                Problem("invalid_smiles", "Cannot convert molecule to SMILES")
            )
            mol = None

        return mol, errors
