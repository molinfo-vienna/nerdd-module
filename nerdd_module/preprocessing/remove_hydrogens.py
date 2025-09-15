"""
Hydrogen removal preprocessing step for molecular data.

This module provides functionality to remove hydrogen atoms from molecular representations, which is
commonly needed for atom-based models that do not predict properties of hydrogen atoms.
"""

import logging
from typing import List, Optional, Tuple

from rdkit.Chem import Mol, RemoveHs

from ..problem import Problem
from .preprocessing_step import PreprocessingStep

__all__ = ["RemoveHydrogens"]

logger = logging.getLogger(__name__)


class RemoveHydrogens(PreprocessingStep):
    """
    Preprocessing step that removes hydrogen atoms from molecules.

    This class removes hydrogen atoms from molecular representations using RDKit's RemoveHs
    function. It provides options for removing only implicit hydrogens, controlling sanitization
    after removal, and handling molecules where hydrogen removal fails.

    Parameters
    ----------
    implicit_only : bool, optional
        If True, only remove implicit hydrogen atoms. If False, remove both implicit and explicit
        hydrogen atoms. Default is False.
    sanitize_after_removal : bool, optional
        If True, sanitize the molecule after hydrogen removal to ensure chemical validity. If False,
        skip sanitization. Default is True.
    remove_invalid_molecules : bool, optional
        If True, molecules where hydrogen removal fails are set to None (removed). If False, the
        original molecule is kept when removal fails. Default is False.

    Examples
    --------
    >>> # Remove all hydrogens with sanitization
    >>> remove_h = RemoveHydrogens()
    >>> # Remove only implicit hydrogens without sanitization
    >>> remove_h = RemoveHydrogens(implicit_only=True, sanitize_after_removal=False)
    >>> # Remove hydrogens and discard molecules where removal fails
    >>> remove_h = RemoveHydrogens(remove_invalid_molecules=True)

    Notes
    -----
    * Hydrogen removal can fail for chemically invalid molecules
    * Implicit hydrogens are those not explicitly represented in the molecular graph, e.g. those
      inferred by RDKit in SMILES strings like "C" or "CCO"
    * Explicit hydrogens are those represented as separate atoms in the molecular graph, e.g. in a
      SMILES string like "C(H)(H)(H)(H)" or "[CH4]"
    """

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
        """
        Remove hydrogen atoms from a molecule.

        Parameters
        ----------
        mol : Mol
            RDKit Mol object representing the molecule from which to remove hydrogens.

        Returns
        -------
        Tuple[Optional[Mol], List[Problem]]
            A tuple containing:
            * The molecule with hydrogens removed, the original molecule if removal failed and
              remove_invalid_molecules is False, or None if removal failed and
              remove_invalid_molecules is True
            * A list containing a Problem if hydrogen removal failed, otherwise an empty list
        """
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
