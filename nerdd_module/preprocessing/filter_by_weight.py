"""
Molecular weight filtering preprocessing step.

This module provides a preprocessing step that filters molecules based on their molecular weight.
This is desirable for models having a runtime scaling with molecule size.
"""

from typing import List, Optional, Tuple

from rdkit.Chem import Mol
from rdkit.Chem.rdMolDescriptors import CalcExactMolWt

from ..problem import InvalidWeightProblem, Problem
from .preprocessing_step import PreprocessingStep

__all__ = ["FilterByWeight"]


class FilterByWeight(PreprocessingStep):
    """
    Preprocessing step that filters molecules based on molecular weight.

    This class validates molecules against specified minimum and maximum molecular weight
    thresholds. Molecules outside these bounds are flagged and optionally removed from the pipeline.

    Parameters
    ----------
    min_weight : float, optional
        Minimum allowed molecular weight in Daltons (Da). Default is 0.
    max_weight : float, optional
        Maximum allowed molecular weight in Daltons (Da). Default is infinity.
    remove_invalid_molecules : bool, optional
        If True, molecules outside the weight range are set to None (removed). If False, invalid
        molecules are kept. Default is False.

    Examples
    --------
    >>> # Filter molecules between 150 and 500 Da, keeping invalid ones
    >>> filter_step = FilterByWeight(min_weight=150, max_weight=500)

    >>> # Filter molecules below 1000 Da, removing invalid ones
    >>> filter_step = FilterByWeight(max_weight=1000, remove_invalid_molecules=True)

    >>> # Only set minimum weight threshold
    >>> filter_step = FilterByWeight(min_weight=100)

    Notes
    -----
    * Even if remove_invalid_molecules is set to False, molecules with invalid weight are still
      marked with a problem instance
    * The molecular weight is calculated using RDKit's CalcExactMolWt function
    """

    def __init__(
        self,
        min_weight: float = 0,
        max_weight: float = float("inf"),
        remove_invalid_molecules: bool = False,
    ) -> None:
        super().__init__()
        self._min_weight = min_weight
        self._max_weight = max_weight
        self._remove_invalid_molecules = remove_invalid_molecules

    def _preprocess(self, mol: Mol) -> Tuple[Optional[Mol], List[Problem]]:
        """
        Filter a molecule based on its molecular weight.

        Calculates the exact molecular weight of the input molecule and validates it against the
        configured minimum and maximum weight thresholds.

        Parameters
        ----------
        mol : Mol
            RDKit Mol object representing the molecule to be validated.

        Returns
        -------
        Tuple[Optional[Mol], List[Problem]]
            A tuple containing:
            * The original molecule if within weight bounds, or None if outside bounds and
              remove_invalid_molecules is True
            * A list containing an InvalidWeightProblem if the molecule is outside the weight
              bounds, otherwise an empty list
        """
        problems = []
        result_mol = mol

        weight = CalcExactMolWt(mol)
        if weight < self._min_weight or weight > self._max_weight:
            if self._remove_invalid_molecules:
                result_mol = None
            problems.append(InvalidWeightProblem(weight, self._min_weight, self._max_weight))

        return result_mol, problems
