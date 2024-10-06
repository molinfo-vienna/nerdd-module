from abc import abstractmethod
from typing import Iterable, Iterator, Union

from .step import Step

__all__ = ["MapStep"]


class MapStep(Step):
    def __init__(self, is_source: bool = False) -> None:
        super().__init__(is_source=is_source)

    def _run(self, source: Iterator[dict]) -> Iterator[dict]:
        # The _process method might return a single result or a list of results and we
        # define a wrapper function to handle both cases. In the first case, we yield
        # the result, in the second case we yield each element of the list.
        def _wrapper(result: Union[dict, Iterable[dict]]) -> Iterator[dict]:
            if isinstance(result, dict):
                yield result
            elif isinstance(result, Iterable):
                # this can be a list, an iterator or a generator
                yield from result
            else:
                # anything that is not a dict or an iterable / generator
                yield result

        # If this transform has no source, then it is the first transform in the chain
        # (i.e. it generates data without input). We call _process with the empty dict
        # as input to start the generation process.
        if self.is_source:
            yield from _wrapper(self._process(dict()))
        else:
            for record in source:
                yield from _wrapper(self._process(record))

    @abstractmethod
    def _process(self, record: dict) -> Union[dict, Iterable[dict]]:
        pass
