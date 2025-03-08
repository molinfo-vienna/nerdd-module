from typing import Any, Iterator

from ..config import Module
from ..output import Writer
from ..steps import OutputStep

__all__ = ["WriteOutputStep"]


class WriteOutputStep(OutputStep):
    def __init__(self, output_format: str, config: Module, **kwargs: Any) -> None:
        super().__init__()
        self._output_format = output_format
        self._config = config
        self._kwargs = kwargs

    def _get_result(self, source: Iterator[dict]) -> Any:
        # get the correct output writer
        writer = Writer.get_writer(self._output_format, config=self._config, **self._kwargs)
        result = writer.write(source)
        return result

    def __repr__(self) -> str:
        return f"WriteOutputStep(output_format={self._output_format}, kwargs={self._kwargs})"
