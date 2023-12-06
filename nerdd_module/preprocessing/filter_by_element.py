from typing import Iterable, List, Tuple

from rdkit.Chem import Mol

from .step import Step


class FilterByElement(Step):
    def __init__(
        self, allowed_elements: Iterable[str], remove_invalid_molecules: bool = False
    ):
        super().__init__()
        self.allowed_elements = set(allowed_elements)
        self.remove_invalid_molecules = remove_invalid_molecules

    def _run(self, mol: Mol) -> Tuple[Mol, List[str]]:
        """
        Sets all molecules with elements that are not in allowedAtomNrs to None.
        """
        errors = []
        result_mol = mol

        atomic_nums = set(atom.GetSymbol() for atom in mol.GetAtoms())
        if len(atomic_nums - self.allowed_elements) > 0:
            if self.remove_invalid_molecules:
                result_mol = None
            errors.append("E1")

        return result_mol, errors
