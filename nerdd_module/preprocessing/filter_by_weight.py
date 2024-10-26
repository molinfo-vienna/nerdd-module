from typing import List, Optional, Tuple

from rdkit.Chem import Mol
from rdkit.Chem.rdMolDescriptors import CalcExactMolWt

from ..problem import InvalidWeightProblem, Problem
from .preprocessing_step import PreprocessingStep


class FilterByWeight(PreprocessingStep):
    def __init__(
        self,
        min_weight: float,
        max_weight: float,
        remove_invalid_molecules: bool = False,
    ) -> None:
        super().__init__()
        self.min_weight = min_weight
        self.max_weight = max_weight
        self.remove_invalid_molecules = remove_invalid_molecules

    def _preprocess(self, mol: Mol) -> Tuple[Optional[Mol], List[Problem]]:
        problems = []
        result_mol = mol

        weight = CalcExactMolWt(mol)
        if weight < self.min_weight or weight > self.max_weight:
            if self.remove_invalid_molecules:
                result_mol = None
            problems.append(InvalidWeightProblem(weight, self.min_weight, self.max_weight))

        return result_mol, problems
