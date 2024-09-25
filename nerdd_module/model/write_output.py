from typing import Iterator, Optional

from ..output import WriterRegistry
from ..steps import Step

__all__ = ["WriteOutput"]


class WriteOutput(Step):
    def __init__(self, output_format: str, **kwargs) -> None:
        super().__init__()
        self._output_format = output_format
        self._kawrgs = kwargs
        self._source: Optional[Iterator[dict]] = None

    def get_result(self):
        assert (
            self._source is not None
        ), "No source data to write. You might need to run the pipeline first."

        # get the correct output writer
        writer = WriterRegistry().get_writer(self._output_format, **self._kawrgs)
        result = writer.write(self._source)

        return result

    def _run(self, source: Iterator[dict]) -> Iterator[dict]:
        self._source = source

        # return an empty iterator to satisfy method return type
        return iter([])
