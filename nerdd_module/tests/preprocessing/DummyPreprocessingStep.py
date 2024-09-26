from typing import List, Optional, Tuple

from rdkit.Chem import Mol

from nerdd_module.preprocessing import PreprocessingStep
from nerdd_module.problem import Problem

__all__ = ["DummyPreprocessingStep"]


class DummyPreprocessingStep(PreprocessingStep):
    def __init__(self, mode):
        super().__init__()

        assert mode in ["error", "do_nothing"]

        self._mode = mode

    def _preprocess(self, mol) -> Tuple[Optional[Mol], List[Problem]]:
        if self._mode == "error":
            raise ValueError("An error occurred.")
        elif self._mode == "do_nothing":
            return mol, []
        else:
            raise ValueError(f"Unknown mode: {self._mode}")
