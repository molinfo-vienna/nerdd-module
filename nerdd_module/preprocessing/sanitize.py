"""
Molecule sanitization preprocessing step for molecular data.

This module provides functionality to sanitize molecular representations using RDKit's sanitization
procedures. Sanitization validates and corrects molecular structures to ensure they are chemically
reasonable and properly formatted.
"""

import logging
from typing import List, Optional, Tuple

from rdkit.Chem import (
    AtomKekulizeException,
    AtomValenceException,
    KekulizeException,
    Mol,
    SanitizeMol,
)

from ..problem import Problem
from .preprocessing_step import PreprocessingStep

__all__ = ["Sanitize"]


logger = logging.getLogger(__name__)


class Sanitize(PreprocessingStep):
    """
    Preprocessing step that sanitizes molecular representations.

    This class applies RDKit's molecule sanitization procedures to validate and correct molecular
    structures. Sanitization includes kekulization, valence checking, aromaticity perception, and
    other chemical validity checks.

    Parameters
    ----------
    None

    Examples
    --------
    >>> # Create a sanitization step
    >>> sanitize_step = Sanitize()

    Notes
    -----
    * Molecules that fail sanitization are always removed (set to None)
    * Different types of sanitization failures generate specific problem codes
      ("kekulization_error" for general kekulization failures, "atom_kekulization_error" for
      atom-specific kekulization failures, "valence_error" for valence validation failures)
    * Other sanitization errors generate a generic problem code "sanitization_error"
    """

    def __init__(self) -> None:
        super().__init__()

    def _preprocess(self, mol: Mol) -> Tuple[Optional[Mol], List[Problem]]:
        """
        Sanitize a molecular representation.

        Applies RDKit's SanitizeMol function to validate and correct the molecular structure.
        Different types of sanitization failures are caught and converted to appropriate problem
        codes.

        Parameters
        ----------
        mol : Mol
            RDKit Mol object representing the molecule to be sanitized.

        Returns
        -------
        Tuple[Optional[Mol], List[Problem]]
            A tuple containing:
            * The sanitized molecule if successful, or None if sanitization failed
            * An empty list if sanitization succeeded, or a list containing a Problem instance
        """
        try:
            SanitizeMol(mol)
            return mol, []
        except KekulizeException:
            return None, [Problem("kekulization_error", "Failed kekulizing the molecule.")]
        except AtomKekulizeException:
            return None, [
                Problem("atom_kekulization_error", "Failed kekulizing an atom in the molecule.")
            ]
        except AtomValenceException as e:
            return None, [Problem("valence_error", str(e))]
        except Exception as e:
            logger.exception(e)
            return None, [Problem("sanitization_error", "Failed sanitizing the molecule.")]
