import zipfile
from typing import Generator

from .reader import MoleculeEntry, Reader
from .reader_registry import register_reader

__all__ = ["ZipReader"]


@register_reader
class ZipReader(Reader):
    def __init__(self):
        super().__init__()

    def read(self, input_stream, explore) -> Generator[MoleculeEntry, None, None]:
        if not hasattr(input_stream, "read") or not hasattr(input_stream, "seek"):
            raise TypeError("input must be a stream-like object")

        input_stream.seek(0)

        with zipfile.ZipFile(input_stream, "r") as zipf:
            for member in zipf.namelist():
                # check if the member is a file
                if member.endswith("/"):
                    continue
                with zipf.open(member, "r") as f:
                    for entry in explore(f):
                        yield entry._replace(source=tuple([member, *entry.source]))

    def __repr__(self) -> str:
        return "ZipReader()"
