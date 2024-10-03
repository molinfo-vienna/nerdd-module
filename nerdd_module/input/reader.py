from __future__ import annotations

import inspect
from abc import ABC, ABCMeta, abstractmethod
from functools import partial
from typing import Callable, Iterator, List, NamedTuple, Optional, Tuple

from rdkit.Chem import Mol

from ..problem import Problem
from ..util import call_with_mappings

__all__ = ["MoleculeEntry", "Reader"]


class MoleculeEntry(NamedTuple):
    raw_input: str
    input_type: str
    source: Tuple[str, ...]
    mol: Optional[Mol]
    errors: List[Problem]


_factories: List[Callable[[dict], Reader]] = []


class ReaderMeta(ABCMeta):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)

        if not inspect.isabstract(cls):
            _factories.append(
                partial(
                    call_with_mappings,
                    cls,
                )
            )


class Reader(ABC, metaclass=ReaderMeta):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def read(self, input, explore) -> Iterator[MoleculeEntry]:
        pass

    @classmethod
    def get_readers(cls, **kwargs) -> List[Reader]:
        return [factory(kwargs) for factory in _factories]
