from abc import ABC, abstractmethod
from typing import BinaryIO, FrozenSet, Generator, List, NamedTuple, Optional

from rdkit.Chem import Mol

__all__ = ["Reader", "MoleculeEntry"]


class MoleculeEntry(NamedTuple):
    raw_input: str
    input_type: str
    source: str
    mol: Optional[Mol]
    errors: List[str]


class Reader(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def read(self, input) -> Generator[MoleculeEntry, None, None]:
        pass

    @property
    def input_type(self) -> str:
        return self._input_type()

    @abstractmethod
    def _input_type(self) -> str:
        pass
