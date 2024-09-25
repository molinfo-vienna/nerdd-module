from abc import abstractmethod
from typing import Iterable, Iterator, List, Optional, Tuple, Union

from rdkit.Chem import Mol

from ..problem import Problem
from ..steps import MapStep

__all__ = ["PreprocessingStep"]


class PreprocessingStep(MapStep):
    def __init__(self):
        super().__init__()

    def _process(self, record: dict) -> Union[dict, Iterable[dict], Iterator[dict]]:
        # If "preprocessed_mol" is not present, then this is the first preprocessing
        # step.
        if "preprocessed_mol" not in record:
            mol = record.get("input_mol")
            record["preprocessed_mol"] = mol

        mol = record["preprocessed_mol"]

        # We don't preprocess invalid molecules.
        if mol is None:
            return record

        mol, problems = self._preprocess(mol)
        record["preprocessed_mol"] = mol

        if "problems" in record:
            record["problems"].extend(problems)
        else:
            record["problems"] = problems

        return record

    @abstractmethod
    def _preprocess(self, mol: Mol) -> Tuple[Optional[Mol], List[Problem]]:
        """
        Runs the preprocesing step on a molecule.
        """
        pass
