import logging
from typing import List, Optional, Tuple

from rdkit.Chem import AtomKekulizeException, KekulizeException, Mol, SanitizeMol

from ..problem import Problem
from .preprocessing_step import PreprocessingStep

__all__ = ["Sanitize"]


logger = logging.getLogger(__name__)


class Sanitize(PreprocessingStep):
    def __init__(self) -> None:
        super().__init__()

    def _preprocess(self, mol: Mol) -> Tuple[Optional[Mol], List[Problem]]:
        try:
            SanitizeMol(mol)
            return mol, []
        except KekulizeException:
            return None, [Problem("kekulization_error", "Failed kekulizing the molecule.")]
        except AtomKekulizeException:
            return None, [
                Problem("atom_kekulization_error", "Failed kekulizing an atom in the molecule.")
            ]
        except Exception as e:
            logger.exception(e)
            return None, [Problem("sanitization_error", "Failed sanitizing the molecule.")]
