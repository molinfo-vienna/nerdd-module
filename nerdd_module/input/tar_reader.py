import tarfile
from typing import Any, Iterator

from .reader import ExploreCallable, MoleculeEntry, Reader

__all__ = ["TarReader"]


class TarReader(Reader):
    def __init__(self) -> None:
        super().__init__()

    def read(self, input_stream: Any, explore: ExploreCallable) -> Iterator[MoleculeEntry]:
        if not hasattr(input_stream, "read") or not hasattr(input_stream, "seek"):
            raise TypeError("input must be a stream-like object")

        input_stream.seek(0)

        with tarfile.open(fileobj=input_stream, mode="r") as tar:
            for member in tar.getmembers():
                if not member.isfile():
                    continue
                for entry in explore(tar.extractfile(member)):
                    yield entry._replace(source=(member.name, *entry.source))

    def __repr__(self) -> str:
        return "TarReader()"
