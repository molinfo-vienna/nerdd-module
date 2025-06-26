from typing import List, Optional, Tuple

from rdkit.Chem import GetMolFrags, Mol
from rdkit.Chem.rdMolDescriptors import CalcExactMolWt

from ..problem import Problem
from .preprocessing_step import PreprocessingStep

__all__ = ["RemoveSmallFragments"]


class RemoveSmallFragments(PreprocessingStep):
    def __init__(
        self,
    ) -> None:
        super().__init__()

    def _preprocess(self, mol: Mol) -> Tuple[Optional[Mol], List[Problem]]:
        fragments = GetMolFrags(mol, asMols=True)
        if len(fragments) > 1:
            # select the largest fragment
            largest_fragment = max(fragments, key=CalcExactMolWt)
        else:
            largest_fragment = mol

        return largest_fragment, []
