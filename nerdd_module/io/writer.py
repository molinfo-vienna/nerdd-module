import codecs
from abc import ABC, abstractmethod
from io import BufferedWriter, TextIOWrapper
from typing import BinaryIO, Dict, Iterable, TextIO, Union

StreamWriter = codecs.getwriter("utf-8")

__all__ = ["Writer"]


class Writer(ABC):
    """Abstract class for writers."""

    @property
    def output_type(self) -> str:
        """The output type of the writer."""
        return self._output_type()

    @abstractmethod
    def _output_type(self) -> str:
        """The output type of the writer."""
        pass

    def write(self, output: Union[BinaryIO, TextIO, str], entries: Iterable[Dict]):
        """Write entries to output."""
        if isinstance(output, str):
            with open(output, "wb") as f:
                self._write(f, entries)
        else:
            self._write(output, entries)
            output.flush()

    @abstractmethod
    def _write(self, output: Union[BinaryIO, TextIO], entries: Iterable[Dict]):
        """Write entries to output."""
        pass
