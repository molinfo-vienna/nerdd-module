import codecs
from abc import abstractmethod
from pathlib import Path
from typing import IO, Any, BinaryIO, Iterable, TextIO, Union

from .writer import Writer

StreamWriter = codecs.getwriter("utf-8")

__all__ = ["FileWriter", "FileLike"]


FileLike = Union[str, Path, TextIO, BinaryIO]


class FileWriter(Writer, is_abstract=True):
    """Abstract class for writers."""

    def __init__(self, output_file: FileLike, writes_bytes: bool = False) -> None:
        self._output_file = output_file
        self._writes_bytes = writes_bytes

    def write(self, entries: Iterable[dict]) -> None:
        """Write entries to output."""
        if isinstance(self._output_file, (str, Path)):
            mode = "wb" if self._writes_bytes else "w"
            with open(self._output_file, mode) as f:
                self._write(f, entries)
        else:
            self._write(self._output_file, entries)
            self._output_file.flush()

    @abstractmethod
    def _write(self, output: IO[Any], entries: Iterable[dict]) -> None:
        """Write entries to output."""
        pass

    @property
    def writes_bytes(self) -> bool:
        """Whether the writer writes bytes."""
        return self._writes_bytes
