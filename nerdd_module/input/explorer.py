from abc import ABC, abstractmethod
from typing import Iterator

from .reader import MoleculeEntry, Reader


class Explorer(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def explore(self, input) -> Iterator[MoleculeEntry]:
        pass

    def _read(self, reader: Reader, input) -> Iterator[MoleculeEntry]:
        return reader.read(input, self.explore)
