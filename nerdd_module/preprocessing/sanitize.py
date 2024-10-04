from typing import List, Optional, Tuple

from rdkit.Chem import Mol, SanitizeMol

from ..problem import Problem
from .preprocessing_step import PreprocessingStep

__all__ = ["Sanitize"]


class Sanitize(PreprocessingStep):
    def __init__(self) -> None:
        super().__init__()

    def _preprocess(self, mol: Mol) -> Tuple[Optional[Mol], List[Problem]]:
        problems: List[Problem] = []

        # sanitize molecule
        SanitizeMol(mol)

        return mol, problems
