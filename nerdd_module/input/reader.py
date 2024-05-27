from abc import ABC, abstractmethod
from typing import Generator, List, NamedTuple, Optional, Tuple

from rdkit.Chem import Mol

from ..problem import Problem

__all__ = ["MoleculeEntry", "Reader"]


class MoleculeEntry(NamedTuple):
    raw_input: str
    input_type: str
    source: Tuple[str, ...]
    mol: Optional[Mol]
    errors: List[Problem]


class Reader(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def read(self, input, explore) -> Generator[MoleculeEntry, None, None]:
        pass
