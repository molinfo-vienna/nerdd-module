"""
Preprocessing step module for molecular data processing.

This module provides the base class for implementing preprocessing steps that can be applied to
molecular data in a processing pipeline. Preprocessing steps operate on molecular records and can
transform, validate, or clean molecular data.
"""

import logging
from abc import abstractmethod
from typing import Iterable, Iterator, List, Optional, Tuple, Union

from rdkit.Chem import Mol

from ..problem import Problem
from ..steps import MapStep

__all__ = ["PreprocessingStep"]


logger = logging.getLogger(__name__)


def UnknownPreprocessingProblem() -> Problem:
    """
    Create a Problem instance for unknown preprocessing errors.

    Returns
    -------
    Problem
        A Problem object representing an unknown preprocessing error with a
        generic error message.
    """
    return Problem("unknown_preprocessing_error", "An unknown error occurred during preprocessing.")


class PreprocessingStep(MapStep):
    """
    Base class for molecular preprocessing steps.

    This abstract class provides the framework for implementing preprocessing steps that operate on
    molecular data records. Each preprocessing step receives a record containing molecular data and
    can transform, validate, or clean the molecule.

    Notes
    -----
    Subclasses must implement the `_preprocess` method to define the specific preprocessing logic
    for their use case.

    Examples
    --------
    >>> class MyPreprocessingStep(PreprocessingStep):
    ...     def _preprocess(self, mol):
    ...         # Custom preprocessing logic here
    ...         return mol, []
    """

    def __init__(self) -> None:
        super().__init__()

    def _process(self, record: dict) -> Union[dict, Iterable[dict], Iterator[dict]]:
        """
        Process a single record through the preprocessing step.

        This method handles the preprocessing pipeline logic, including molecule extraction,
        preprocessing execution, error handling, and problem accumulation.

        Parameters
        ----------
        record : dict
            A dictionary containing molecular data. Expected to have either "input_mol" (for first
            preprocessing step) or "preprocessed_mol" (for subsequent steps). May also contain a
            "problems" list.

        Returns
        -------
        dict
            The processed record with updated "preprocessed_mol" field and accumulated "problems"
            list. If preprocessing fails, the molecule will be set to None and problems will be
            added.

        Notes
        -----
        * If "preprocessed_mol" is not present, the molecule is taken from "input_mol"
        * Invalid (None) molecules are not preprocessed but passed through unchanged
        * Any exceptions during preprocessing are caught and converted to problems
        * Problems are accumulated in the record's "problems" list
        """
        # if "preprocessed_mol" is not present, then this is the first preprocessing step
        if "preprocessed_mol" not in record:
            mol = record.get("input_mol")
            record["preprocessed_mol"] = mol

        mol = record["preprocessed_mol"]

        # don't preprocess invalid molecules
        if mol is None:
            return record

        try:
            # run the actual preprocessing step
            mol, problems = self._preprocess(mol)
        except Exception as e:
            logger.exception("Unknown exception occured during preprocessing", exc_info=e)

            mol = None
            problems = [UnknownPreprocessingProblem()]

        record["preprocessed_mol"] = mol

        if "problems" in record:
            record["problems"].extend(problems)
        else:
            record["problems"] = problems

        return record

    @abstractmethod
    def _preprocess(self, mol: Mol) -> Tuple[Optional[Mol], List[Problem]]:
        """
        Run the preprocessing step on a molecule.

        This abstract method must be implemented by subclasses to define the specific preprocessing
        logic for their use case.

        Parameters
        ----------
        mol : Mol
            An RDKit Mol object representing the molecule to be preprocessed. It is guaranteed to
            be not None when this method is called.

        Returns
        -------
        Tuple[Optional[Mol], List[Problem]]
            A tuple containing:
            * The preprocessed molecule (Mol object) or None if preprocessing failed
            * A list of Problem objects describing any issues encountered during preprocessing.
        """
        ...
