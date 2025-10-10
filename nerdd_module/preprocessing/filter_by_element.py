"""
Element filtering preprocessing step for molecular data.

This module provides functionality to filter molecules based on their elemental composition,
allowing only molecules containing specified allowed elements to pass through the processing
pipeline.
"""

from typing import Iterable, List, Optional, Set, Tuple

from rdkit.Chem import Mol

from ..problem import InvalidElementsProblem, Problem
from .preprocessing_step import PreprocessingStep

__all__ = ["FilterByElement", "ORGANIC_SUBSET"]

ORGANIC_SUBSET = [
    "H",
    "B",
    "C",
    "N",
    "O",
    "F",
    "Si",
    "P",
    "S",
    "Cl",
    "Se",
    "Br",
    "I",
]
"""
List[str] : Predefined set of elements commonly found in organic molecules.

This list contains the atomic symbols of elements that are typically present in organic and
drug-like molecules. It can be used as a convenient preset for the FilterByElement class to restrict
molecules to organic chemistry space.

The elements included are:
* H (Hydrogen)
* B (Boron)
* C (Carbon)
* N (Nitrogen)
* O (Oxygen)
* F (Fluorine)
* Si (Silicon)
* P (Phosphorus)
* S (Sulfur)
* Cl (Chlorine)
* Se (Selenium)
* Br (Bromine)
* I (Iodine)

Examples
--------
>>> filter_step = FilterByElement(ORGANIC_SUBSET)
>>> # This will only allow molecules containing organic elements
"""


class FilterByElement(PreprocessingStep):
    """
    Preprocessing step that filters molecules based on elemental composition.

    This class validates molecules against a specified set of allowed elements. Molecules containing
    elements not in the allowed set are flagged with a problem instance "invalid_element" and
    optionally removed from the pipeline.

    Parameters
    ----------
    allowed_elements : Iterable[str]
        An iterable of atomic symbols (element names) that are allowed in molecules. Element symbols
        are case-insensitive but will be normalized to proper case (first letter uppercase, rest
        lowercase).
    remove_invalid_molecules : bool, optional
        If True, molecules containing disallowed elements are set to None (removed). If False,
        invalid molecules are kept. Default is False.

    Examples
    --------
    >>> # Allow only carbon, nitrogen, oxygen, and hydrogen
    >>> filter_step = FilterByElement(['C', 'N', 'O', 'H'])

    >>> # Use predefined organic subset, removing invalid molecules
    >>> filter_step = FilterByElement(ORGANIC_SUBSET, remove_invalid_molecules=True)

    Notes
    -----
    * Element symbols are normalized to proper case (e.g., 'cl' becomes 'Cl')
    * Even if remove_invalid_molecules is set to False, molecules with invalid elements are still
      marked with a problem instance
    * Hydrogen atoms are handled specially since they may not be explicit in the molecular
      representation and are detected via GetTotalNumHs()
    """

    def __init__(
        self, allowed_elements: Iterable[str], remove_invalid_molecules: bool = False
    ) -> None:
        super().__init__()
        self._allowed_elements = {a[0].upper() + a[1:] for a in allowed_elements}
        self._hydrogen_in_allowed_elements = "H" in self._allowed_elements
        self._remove_invalid_molecules = remove_invalid_molecules

    def _preprocess(self, mol: Mol) -> Tuple[Optional[Mol], List[Problem]]:
        """
        Filter a molecule by comparing its elemental composition against allowed elements.

        Parameters
        ----------
        mol : Mol
            RDKit Mol object representing the molecule to be validated.

        Returns
        -------
        Tuple[Optional[Mol], List[Problem]]
            A tuple containing:
            * The original molecule if all elements are allowed, or None if disallowed elements are
              found and remove_invalid_molecules is True
            * A list containing an InvalidElementsProblem if disallowed elements are found,
              otherwise an empty list

        Notes
        -----
        Hydrogen detection is special-cased because hydrogen atoms are often implicit in molecular
        representations and detected via atom.GetTotalNumHs().
        """
        problems = []
        result_mol = mol

        elements: Set[str] = {atom.GetSymbol() for atom in mol.GetAtoms()}
        invalid_elements = elements - self._allowed_elements

        # special case: hydrogens are not recognized by mol.GetAtoms()
        if not self._hydrogen_in_allowed_elements:
            # get the number of hydrogens in mol
            for a in mol.GetAtoms():
                if a.GetTotalNumHs() > 0:
                    invalid_elements.add("H")
                    break

        if len(invalid_elements) > 0:
            if self._remove_invalid_molecules:
                result_mol = None

            problems.append(InvalidElementsProblem(invalid_elements))

        return result_mol, problems
