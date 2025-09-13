import logging
from typing import List, Optional, Tuple

from rdkit.Chem import Mol, RemoveHs

from ..problem import Problem
from .preprocessing_step import PreprocessingStep

__all__ = ["RemoveHydrogens"]

logger = logging.getLogger(__name__)


class RemoveHydrogens(PreprocessingStep):
    def __init__(
        self,
        implicit_only: bool = False,
        sanitize_after_removal: bool = True,
        remove_invalid_molecules: bool = False,
    ) -> None:
        super().__init__()
        self._implicit_only = implicit_only
        self._sanitize_after_removal = sanitize_after_removal
        self._remove_invalid_molecules = remove_invalid_molecules

    def _preprocess(self, mol: Mol) -> Tuple[Optional[Mol], List[Problem]]:
        problems: List[Problem] = []

        try:
            result_mol = RemoveHs(
                mol, implicitOnly=self._implicit_only, sanitize=self._sanitize_after_removal
            )
        except Exception as e:
            logger.exception("Could not remove hydrogens from molecule.", exc_info=e)
            problems.append(
                Problem("invalid_molecule", "Could not remove hydrogens from molecule.")
            )
            if self._remove_invalid_molecules:
                result_mol = None
            else:
                result_mol = mol

        return result_mol, problems
