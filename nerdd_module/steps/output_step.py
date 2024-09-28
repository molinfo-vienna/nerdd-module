from abc import abstractmethod
from typing import Any, Iterator, Optional

from .step import Step


class OutputStep(Step):
    def __init__(self) -> None:
        super().__init__()
        self._source: Optional[Iterator[dict]] = None

    def get_result(self) -> Any:
        assert (
            self._source is not None
        ), "No source data to write. You might need to run the pipeline first."

        return self._get_result(self._source)

    @abstractmethod
    def _get_result(self, source: Iterator[dict]) -> Any:
        pass

    def _run(self, source: Iterator[dict]) -> Iterator[dict]:
        self._source = source

        # return an empty iterator to satisfy method return type
        return iter([])
