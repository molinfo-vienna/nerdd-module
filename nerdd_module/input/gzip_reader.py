import gzip
from typing import Generator

from .reader import MoleculeEntry, Reader
from .reader_registry import register_reader

__all__ = ["GzipReader"]


@register_reader
class GzipReader(Reader):
    def __init__(self):
        super().__init__()

    def read(self, input_stream, explore) -> Generator[MoleculeEntry, None, None]:
        if not hasattr(input_stream, "read") or not hasattr(input_stream, "seek"):
            raise TypeError("input must be a stream-like object")

        input_stream.seek(0)

        with gzip.open(input_stream, "rb") as f:
            # gzip.open will not raise an exception if the file is not a valid gzip file
            # --> check by attempting to read the first byte
            f.read(1)
            f.seek(0)

            yield from explore(f)

    def __repr__(self) -> str:
        return "GzipReader()"
