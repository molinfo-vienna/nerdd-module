"""
Fragment removal preprocessing step for molecular data.

This module provides functionality to remove small molecular fragments by keeping only the largest
fragment when a molecule contains multiple disconnected components. This is commonly used to clean
molecular datasets by removing salts, solvents, and other small fragments.
"""

from typing import List, Optional, Tuple

from rdkit.Chem import GetMolFrags, Mol
from rdkit.Chem.rdMolDescriptors import CalcExactMolWt

from ..problem import Problem
from .preprocessing_step import PreprocessingStep

__all__ = ["RemoveSmallFragments"]


class RemoveSmallFragments(PreprocessingStep):
    """
    Preprocessing step that removes small molecular fragments.

    This class processes molecules that may contain multiple disconnected components (fragments) and
    retains only the largest fragment based on molecular weight. This is useful for removing salts,
    counterions, solvents, and other small molecules that may be present in molecular datasets.

    Parameters
    ----------
    None

    Examples
    --------
    >>> # Create a fragment removal step
    >>> remove_fragments = RemoveSmallFragments()

    >>> # This will process molecules like "CCO.Na+" and return only "CCO"
    >>> # (keeping the ethanol and removing the sodium ion)

    Notes
    -----
    The largest fragment is determined by exact molecular weight (CalcExactMolWt).
    """

    def __init__(
        self,
    ) -> None:
        super().__init__()

    def _preprocess(self, mol: Mol) -> Tuple[Optional[Mol], List[Problem]]:
        """
        Remove small fragments from a molecule, keeping only the largest.

        Identifies all disconnected molecular fragments and returns the fragment with the highest
        molecular weight. If the molecule contains only one fragment, it is returned unchanged.

        Parameters
        ----------
        mol : Mol
            RDKit Mol object representing the molecule to be processed.

        Returns
        -------
        Tuple[Optional[Mol], List[Problem]]
            A tuple containing:
            * The largest molecular fragment (by weight) in the original molecule
            * An empty list (no problems are reported by this step)
        """
        fragments = GetMolFrags(mol, asMols=True)
        if len(fragments) > 1:
            # select the largest fragment
            largest_fragment = max(fragments, key=CalcExactMolWt)
        else:
            largest_fragment = mol

        return largest_fragment, []
