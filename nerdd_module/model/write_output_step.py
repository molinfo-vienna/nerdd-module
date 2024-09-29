from typing import Any, Iterator

from ..output import WriterRegistry
from ..steps import OutputStep

__all__ = ["WriteOutputStep"]


class WriteOutputStep(OutputStep):
    def __init__(self, output_format: str, **kwargs) -> None:
        super().__init__()
        self._output_format = output_format
        self._kawrgs = kwargs

    def _get_result(self, source: Iterator[dict]) -> Any:
        # get the correct output writer
        writer = WriterRegistry().get_writer(self._output_format, **self._kawrgs)
        result = writer.write(source)
        return result
