from abc import ABC, abstractmethod
from typing import List, Tuple

from rdkit.Chem import Mol

__all__ = ["Step"]


class Step(ABC):
    def __init__(self):
        pass

    def run(self, mol: Mol) -> Tuple[Mol, List[str]]:
        """
        Runs the step on a molecule.
        """
        return self._run(mol)

    @abstractmethod
    def _run(self, mol: Mol) -> Tuple[Mol, List[str]]:
        """
        Runs the step on a molecule.
        """
        pass
