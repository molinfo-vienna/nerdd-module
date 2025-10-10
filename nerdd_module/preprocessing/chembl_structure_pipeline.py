"""
ChEMBL Structure Pipeline preprocessing steps for molecular data.

This module provides preprocessing steps that utilize the ChEMBL Structure Pipeline library for
molecule standardization and parent molecule extraction.
"""

import warnings
from typing import List, Optional, Tuple

from rdkit.Chem import Mol

from ..polyfills import BlockLogs
from ..problem import Problem
from .preprocessing_step import PreprocessingStep

# before importing chembl_structure_pipeline, we need to suppress RDKit warnings
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    module="rdkit.Chem.MolStandardize",
)

# We check if chembl_structure_pipeline is installed. Since importing this library already logs
# messages, we suppress them using RDKit's BlockLogs.
with BlockLogs():
    try:
        from chembl_structure_pipeline import get_parent_mol, standardize_mol

        import_error = None
    except ImportError as e:
        # raise ImportError later when using this class
        # --> this allows to use the rest of the package without chembl_structure_pipeline
        import_error = e

__all__ = ["GetParentMolWithCsp", "StandardizeWithCsp"]


class StandardizeWithCsp(PreprocessingStep):
    """
    Preprocessing step that standardizes molecules using ChEMBL Structure Pipeline.

    This class applies the ChEMBL Structure Pipeline standardization procedures to normalize
    molecular representations. The standardization includes tautomer normalization, charge
    neutralization, and other structural standardizations commonly used in pharmaceutical databases.

    Parameters
    ----------
    None

    Raises
    ------
    ImportError
        If the chembl_structure_pipeline library is not installed.

    Examples
    --------
    >>> # Create a standardization step (requires chembl_structure_pipeline)
    >>> standardize_step = StandardizeWithCsp()

    Notes
    -----
    * Requires the chembl_structure_pipeline library to be installed
    * Automatically removes 3D conformers as the pipeline cannot handle them
    * Uses ChEMBL's standardize_mol function which applies comprehensive molecular standardization
      procedures
    * If standardization fails, the original molecule is returned with a problem
    """

    def __init__(self) -> None:
        super().__init__()

        if import_error is not None:
            raise import_error

    def _preprocess(self, mol: Mol) -> Tuple[Optional[Mol], List[Problem]]:
        """
        Standardize a molecule using ChEMBL Structure Pipeline.

        Applies ChEMBL's standardization procedures to normalize the molecular representation. The
        process removes 3D conformers before applying the standardize_mol function.

        Parameters
        ----------
        mol : Mol
            RDKit Mol object representing the molecule to be standardized.

        Returns
        -------
        Tuple[Optional[Mol], List[Problem]]
            A tuple containing:
            * The standardized molecule if successful, or the original molecule if standardization
              failed
            * An empty list if standardization succeeded, or a list containing a Problem instance
              with code "csp_error" if standardization failed
        """
        problems: List[Problem] = []

        # chembl structure pipeline cannot handle molecules with 3D coordinates
        # --> delete conformers
        mol.RemoveAllConformers()

        # standardization via chembl structure pipeline
        preprocessed_mol = standardize_mol(mol)

        if preprocessed_mol is None:
            problems.append(Problem("csp_error", "Could not standardize the molecule."))
            preprocessed_mol = mol

        return preprocessed_mol, problems


class GetParentMolWithCsp(PreprocessingStep):
    """
    Preprocessing step that extracts parent molecules using ChEMBL Structure Pipeline.

    This class uses the ChEMBL Structure Pipeline to identify and extract the parent molecule from
    complex molecular structures. This process removes salts, solvents, and other fragments while
    applying ChEMBL's standardization rules.

    Parameters
    ----------
    None

    Raises
    ------
    ImportError
        If the chembl_structure_pipeline library is not installed.

    Examples
    --------
    >>> # Create a parent molecule extraction step
    >>> get_parent_step = GetParentMolWithCsp()

    Notes
    -----
    * Requires the chembl_structure_pipeline library to be installed
    * Automatically removes 3D conformers as the pipeline cannot handle them
    * Applies the get_parent_mol function from the chembl_structure_pipeline library
    * If parent extraction fails or is flagged for exclusion, the original molecule is returned with
      a Problem instance
    """

    def __init__(self) -> None:
        super().__init__()

        if import_error is not None:
            raise import_error

    def _preprocess(self, mol: Mol) -> Tuple[Optional[Mol], List[Problem]]:
        """
        Extract the parent molecule using ChEMBL Structure Pipeline.

        Identifies and returns the main molecular component. The process removes 3D conformers,
        because chembl_structure_pipeline cannot handle them.

        Parameters
        ----------
        mol : Mol
            RDKit Mol object representing the molecule from which to extract the parent structure.

        Returns
        -------
        Tuple[Optional[Mol], List[Problem]]
            A tuple containing:
            * The parent molecule if successful, or the original molecule if extraction failed
            * An empty list if extraction succeeded, or a list containing a Problem instance with
              code "csp_error" if extraction failed or was flagged for exclusion
        """
        problems = []

        # chembl structure pipeline cannot handle molecules with 3D coordinates
        # --> delete conformers
        mol.RemoveAllConformers()

        # get parent molecule via chembl structure pipeline
        preprocessed_mol, exclude_flag = get_parent_mol(mol)
        if exclude_flag or preprocessed_mol is None:
            problems.append(Problem("csp_error", "Could not remove small fragments."))
        if preprocessed_mol is None:
            preprocessed_mol = mol

        return preprocessed_mol, problems
