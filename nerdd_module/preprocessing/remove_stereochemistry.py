"""
Stereochemistry removal preprocessing step for molecular data.

This module provides functionality to remove stereochemical information from molecular
representations, converting molecules to their non-stereoisomeric forms. This is useful for
models that cannot handle stereochemistry or  where stereochemical information is not relevant.
"""

import logging
from typing import List, Tuple

from rdkit.Chem import Mol
from rdkit.Chem import RemoveStereochemistry as remove_stereochemistry

from ..problem import Problem
from .preprocessing_step import PreprocessingStep

__all__ = ["RemoveStereochemistry"]

logger = logging.getLogger(__name__)


class RemoveStereochemistry(PreprocessingStep):
    """
    Preprocessing step that removes stereochemical information from molecules.

    This class removes all stereochemical information from molecular representations, including
    chiral centers, double bond geometry (E/Z), and other stereoisomeric features. The resulting
    molecules retain their connectivity but lose spatial arrangement information.

    Parameters
    ----------
    None

    Examples
    --------
    >>> # Create a stereochemistry removal step
    >>> remove_stereo = RemoveStereochemistry()
    """

    def __init__(self) -> None:
        super().__init__()

    def _preprocess(self, mol: Mol) -> Tuple[Mol, List[Problem]]:
        """
        Remove stereochemical information from a molecule.

        Applies RDKit's RemoveStereochemistry function to eliminate all stereochemical annotations
        from the input molecule, including chiral centers and double bond geometry.

        Parameters
        ----------
        mol : Mol
            RDKit Mol object representing the molecule from which to remove stereochemical
            information.

        Returns
        -------
        Tuple[Mol, List[Problem]]
            A tuple containing:
            * The input molecule with stereochemistry removed
            * A list containing one problem instance if stereochemistry removal failed, otherwise
              an empty list

        Notes
        -----
        The method uses RDKit's RemoveStereochemistry function which removes chiral center
        annotations (R/S configurations) as well as double bond geometry annotations
        (E/Z configurations) .
        """
        problems = []

        try:
            remove_stereochemistry(mol)
        except Exception as e:
            logger.exception("Cannot remove stereochemistry", exc_info=e)
            problems.append(
                Problem("remove_stereochemistry_failed", "Could not remove stereochemistry.")
            )

        return mol, problems
