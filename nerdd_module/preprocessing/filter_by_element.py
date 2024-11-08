from typing import Iterable, List, Optional, Set, Tuple

from rdkit.Chem import Mol

from ..problem import InvalidElementsProblem, Problem
from .preprocessing_step import PreprocessingStep

__all__ = ["FilterByElement", "ORGANIC_SUBSET"]

ORGANIC_SUBSET = [
    "H",
    "B",
    "C",
    "N",
    "O",
    "F",
    "Si",
    "P",
    "S",
    "Cl",
    "Se",
    "Br",
    "I",
]


class FilterByElement(PreprocessingStep):
    def __init__(
        self, allowed_elements: Iterable[str], remove_invalid_molecules: bool = False
    ) -> None:
        super().__init__()
        self.allowed_elements = {a[0].upper() + a[1:] for a in allowed_elements}
        self.hydrogen_in_allowed_elements = "H" in self.allowed_elements
        self.remove_invalid_molecules = remove_invalid_molecules

    def _preprocess(self, mol: Mol) -> Tuple[Optional[Mol], List[Problem]]:
        problems = []
        result_mol = mol

        elements: Set[str] = {atom.GetSymbol() for atom in mol.GetAtoms()}
        invalid_elements = elements - self.allowed_elements

        # special case: hydrogens are not recognized by mol.GetAtoms()
        if not self.hydrogen_in_allowed_elements:
            # get the number of hydrogens in mol
            for a in mol.GetAtoms():
                if a.GetTotalNumHs() > 0:
                    invalid_elements.add("H")
                    break

        if len(invalid_elements) > 0:
            if self.remove_invalid_molecules:
                result_mol = None

            problems.append(InvalidElementsProblem(invalid_elements))

        return result_mol, problems
