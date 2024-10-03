from abc import ABC, abstractmethod
from typing import Any, Iterator

from .reader import MoleculeEntry, Reader


class Explorer(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def explore(self, input: Any) -> Iterator[MoleculeEntry]:
        pass

    def _read(self, reader: Reader, input: Any) -> Iterator[MoleculeEntry]:
        return reader.read(input, self.explore)
