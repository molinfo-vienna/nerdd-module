import codecs
from abc import ABC, abstractmethod
from io import BufferedWriter, TextIOWrapper
from typing import BinaryIO, Dict, Iterable, TextIO, Union

StreamWriter = codecs.getwriter("utf-8")

__all__ = ["Writer"]


class Writer(ABC):
    """Abstract class for writers."""

    def __init__(self, writes_bytes: bool = False):
        self._writes_bytes = writes_bytes

    @property
    def output_type(self) -> str:
        """The output type of the writer."""
        return self._output_type()

    @abstractmethod
    def _output_type(self) -> str:
        """The output type of the writer."""
        pass

    def write(self, output, entries: Iterable[Dict]):
        """Write entries to output."""
        if isinstance(output, str):
            mode = "wb" if self._writes_bytes else "w"
            with open(output, mode) as f:
                self._write(f, entries)
        else:
            self._write(output, entries)
            output.flush()

    @abstractmethod
    def _write(self, output, entries: Iterable[Dict]):
        """Write entries to output."""
        pass

    @property
    def writes_bytes(self) -> bool:
        """Whether the writer writes bytes."""
        return self._writes_bytes
