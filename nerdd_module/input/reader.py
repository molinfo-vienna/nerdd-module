from __future__ import annotations

import inspect
from abc import ABC, abstractmethod
from typing import Any, Callable, Iterator, List, NamedTuple, Optional, Tuple, Type

from rdkit.Chem import Mol

from ..problem import Problem
from ..util import call_with_mappings

__all__ = ["MoleculeEntry", "Reader", "ExploreCallable"]


class MoleculeEntry(NamedTuple):
    raw_input: str
    input_type: str
    source: Tuple[str, ...]
    mol: Optional[Mol]
    errors: List[Problem]


ExploreCallable = Callable[[Any], Iterator[MoleculeEntry]]


_factories: List[Type["Reader"]] = []


class Reader(ABC):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def __init_subclass__(
        cls,
        **kwargs: Any,
    ) -> None:
        super().__init_subclass__(**kwargs)
        if not inspect.isabstract(cls):
            _factories.append(cls)

    @abstractmethod
    def read(self, input: Any, explore: ExploreCallable) -> Iterator[MoleculeEntry]:
        pass

    @classmethod
    def get_reader_mapping(cls: Type[Reader]) -> List[Type["Reader"]]:
        return _factories

    @classmethod
    def get_readers(cls: Type[Reader], **kwargs: Any) -> List[Reader]:
        return [call_with_mappings(factory, kwargs) for factory in _factories]
