from abc import ABC, abstractmethod
from typing import Generator

from .reader import MoleculeEntry


class Explorer(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def explore(self, input) -> Generator[MoleculeEntry, None, None]:
        pass
