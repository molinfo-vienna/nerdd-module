from typing import Iterable, List, Tuple

from rdkit.Chem import Mol

from ..problem import Problem
from .step import Step


class FilterByElement(Step):
    def __init__(
        self, allowed_elements: Iterable[str], remove_invalid_molecules: bool = False
    ):
        super().__init__()
        self.allowed_elements = set(allowed_elements)
        self.remove_invalid_molecules = remove_invalid_molecules

    def _run(self, mol: Mol) -> Tuple[Mol, List[Problem]]:
        errors = []
        result_mol = mol

        elements = set(atom.GetSymbol() for atom in mol.GetAtoms())
        invalid_elements = elements - self.allowed_elements
        if len(elements - self.allowed_elements) > 0:
            if self.remove_invalid_molecules:
                result_mol = None

            if len(invalid_elements) > 3:
                invalid_elements_str = ", ".join(list(invalid_elements)[:3]) + "..."
            else:
                invalid_elements_str = ", ".join(list(invalid_elements))

            errors.append(
                Problem(
                    "invalid_elements",
                    f"Molecule contains invalid elements {invalid_elements_str}",
                )
            )

        return result_mol, errors
