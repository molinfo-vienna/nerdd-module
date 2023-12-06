from typing import List, Tuple

from rdkit.Chem import Mol
from rdkit.Chem.Descriptors import MolWt

from .step import Step


class FilterByWeight(Step):
    def __init__(self, min_weight, max_weight, remove_invalid_molecules=False):
        super().__init__()
        self.min_weight = min_weight
        self.max_weight = max_weight
        self.remove_invalid_molecules = remove_invalid_molecules

    def _run(self, mol: Mol) -> Tuple[Mol, List[str]]:
        errors = []

        weight = MolWt(mol)
        if weight < self.min_weight or weight > self.max_weight:
            if self.remove_invalid_molecules:
                result_mol = None
            else:
                result_mol = mol
            errors.append("W1")
        else:
            result_mol = mol

        return result_mol, errors
