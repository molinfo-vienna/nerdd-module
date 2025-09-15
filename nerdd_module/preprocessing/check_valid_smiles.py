"""
SMILES validation preprocessing step for molecular data.

This module provides functionality to validate molecular representations by converting them to
SMILES format and attempting to parse them back. This round-trip validation ensures that molecules
can be properly serialized and deserialized as SMILES strings.
"""

from typing import List, Optional, Tuple

from rdkit.Chem import Mol, MolFromSmiles, MolToSmiles

from ..problem import InvalidSmiles, Problem
from .preprocessing_step import PreprocessingStep

__all__ = ["CheckValidSmiles"]


class CheckValidSmiles(PreprocessingStep):
    """
    Preprocessing step that validates molecules through SMILES round-trip conversion.

    This class validates molecular representations by converting them to SMILES format and then
    attempting to parse the SMILES back to a molecule object. This round-trip validation ensures
    that molecules can be properly represented as SMILES strings, which is an indicator for a valid
    molecular structure. Molecules that fail the round-trip test are considered invalid and removed.

    Parameters
    ----------
    None

    Examples
    --------
    >>> # Create a SMILES validation step
    >>> smiles_check = CheckValidSmiles()
    """

    def __init__(self) -> None:
        super().__init__()

    def _preprocess(self, mol: Mol) -> Tuple[Optional[Mol], List[Problem]]:
        """
        Validate a molecule through SMILES round-trip conversion.

        Converts the input molecule to a canonical SMILES string and then attempts to parse it back
        to a molecule object. If the round-trip conversion fails, the molecule is considered
        invalid.

        Parameters
        ----------
        mol : Mol
            RDKit Mol object representing the molecule to be validated.

        Returns
        -------
        Tuple[Optional[Mol], List[Problem]]
            A tuple containing:
            * The original molecule if SMILES validation succeeded, or None if validation failed
            * An empty list if validation succeeded, or a list containing an InvalidSmiles problem
              if validation failed

        Notes
        -----
        The validation process converts the molecule to canonical SMILES.
        """
        problems = []

        smi = MolToSmiles(mol, True)
        check_mol = MolFromSmiles(smi)
        if check_mol is None:
            problems.append(InvalidSmiles())
            mol = None

        return mol, problems
