from typing import Any, Iterator

from ..output import Writer
from ..steps import OutputStep

__all__ = ["WriteOutputStep"]


class WriteOutputStep(OutputStep):
    def __init__(self, output_format: str, **kwargs: Any) -> None:
        super().__init__()
        self._output_format = output_format
        self._kawrgs = kwargs

    def _get_result(self, source: Iterator[dict]) -> Any:
        # get the correct output writer
        writer = Writer.get_writer(self._output_format, **self._kawrgs)
        result = writer.write(source)
        return result

    def __repr__(self) -> str:
        return f"WriteOutputStep(output_format={self._output_format}, kwargs={self._kawrgs})"
