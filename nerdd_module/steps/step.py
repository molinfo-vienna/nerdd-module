from abc import ABC, abstractmethod
from typing import Iterator, Optional

__all__ = ["Step"]


class Step(ABC):
    def __init__(self, is_source: bool = False) -> None:
        self._is_source = is_source

    @property
    def is_source(self) -> bool:
        return self._is_source

    def __call__(self, source: Optional[Iterator[dict]] = None) -> Iterator[dict]:
        assert self.is_source == (
            source is None
        ), "No source was given and this step is not a source."

        if source is not None:
            return self._run(source)
        else:
            return self._run(iter([]))

    @abstractmethod
    def _run(self, source: Iterator[dict]) -> Iterator[dict]:
        pass
