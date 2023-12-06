from abc import ABC, abstractmethod
from typing import BinaryIO, Generator, Iterable, List, Optional, Tuple

from rdkit.Chem import Mol

from .reader import MoleculeEntry, Reader


class ElementaryReader(Reader):
    def __init__(self):
        super().__init__()

    def read(self, input):
        if input is not None:
            mol, errors = self._read(input)
        else:
            mol = None
            errors = ["!1"]

        yield MoleculeEntry(
            raw_input=input,
            input_type=self.input_type,
            source="raw_input",
            mol=mol,
            errors=list(errors),
        )

    @abstractmethod
    def _read(self, input) -> Tuple[Optional[Mol], Iterable[str]]:
        pass
