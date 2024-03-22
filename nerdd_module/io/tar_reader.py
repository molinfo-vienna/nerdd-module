import tarfile
from typing import Generator

from .reader import MoleculeEntry, Reader
from .reader_registry import register_reader

__all__ = ["TarReader"]


@register_reader
class TarReader(Reader):
    def __init__(self):
        super().__init__()

    def read(self, input_stream, explore) -> Generator[MoleculeEntry, None, None]:
        if not hasattr(input_stream, "read") or not hasattr(input_stream, "seek"):
            raise TypeError("input must be a stream-like object")

        input_stream.seek(0)

        with tarfile.open(fileobj=input_stream, mode="r") as tar:
            for member in tar.getmembers():
                if not member.isfile():
                    continue
                for entry in explore(tar.extractfile(member)):
                    yield entry._replace(source=tuple([member.name, *entry.source]))

    def __repr__(self) -> str:
        return "TarReader()"
