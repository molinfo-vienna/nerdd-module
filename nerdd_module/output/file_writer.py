import codecs
from abc import abstractmethod
from io import BufferedIOBase, TextIOBase, TextIOWrapper
from pathlib import Path
from typing import IO, Any, BinaryIO, Iterable, TextIO, Union

from .writer import Writer
from .writer_config import WriterConfig

StreamWriter = codecs.getwriter("utf-8")

__all__ = ["FileWriter", "FileLike"]


FileLike = Union[str, Path, TextIO, BinaryIO]


def is_bytes_stream(stream: Union[TextIO, BinaryIO]) -> bool:
    if hasattr(stream, "buffer"):
        return False
    else:
        return True


class FileWriter(Writer):
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
            if self._writes_bytes == is_bytes_stream(self._output_file):
                stream = self._output_file
            elif self._writes_bytes:
                # underlying writer expects str (but the writer wants to write bytes)
                assert isinstance(self._output_file, TextIOBase) and hasattr(
                    self._output_file, "buffer"
                )
                stream = self._output_file.buffer
            elif not self._writes_bytes:
                # underlying writer expects bytes (but the writer wants to write str)
                assert isinstance(self._output_file, BufferedIOBase)
                stream = TextIOWrapper(self._output_file, encoding="utf-8")

            self._write(stream, entries)
            stream.flush()

    @abstractmethod
    def _write(self, output: IO[Any], entries: Iterable[dict]) -> None:
        """Write entries to output."""
        pass

    @property
    def writes_bytes(self) -> bool:
        """Whether the writer writes bytes."""
        return self._writes_bytes

    config = WriterConfig(is_abstract=True, output_format="file")
