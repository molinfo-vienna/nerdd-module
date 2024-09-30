from rdkit.Chem import SanitizeMol, Mol
from typing import List, Optional, Tuple
from ..problem import Problem

from .preprocessing_step import PreprocessingStep

__all__ = ["Sanitize"]


class Sanitize(PreprocessingStep):
    def __init__(self):
        super().__init__()

    def _preprocess(self, mol: Mol) -> Tuple[Optional[Mol], List[Problem]]:
        problems: List[Problem] = []

        # sanitize molecule
        SanitizeMol(mol)

        return mol, problems
