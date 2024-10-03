from __future__ import annotations

import inspect
from abc import ABC, ABCMeta, abstractmethod
from functools import partial
from typing import Any, Callable, Iterator, List, NamedTuple, Optional, Tuple, Type

from rdkit.Chem import Mol
from typing_extensions import Protocol

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


class ReaderFactory(Protocol):
    def __call__(self, config: dict, *args: Any, **kwargs: Any) -> Reader: ...


_factories: List[ReaderFactory] = []


class ReaderMeta(ABCMeta):
    def __init__(cls, name: str, bases: Tuple[type, ...], dct: dict) -> None:
        super().__init__(name, bases, dct)

        if not inspect.isabstract(cls):
            _factories.append(
                partial(
                    call_with_mappings,
                    cls,
                )
            )


class Reader(ABC, metaclass=ReaderMeta):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def read(self, input: Any, explore: ExploreCallable) -> Iterator[MoleculeEntry]:
        pass

    @classmethod
    def get_readers(cls: Type[Reader], **kwargs: Any) -> List[Reader]:
        return [factory(kwargs) for factory in _factories]
