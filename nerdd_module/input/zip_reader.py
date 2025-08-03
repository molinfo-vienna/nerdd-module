import zipfile
from typing import Any, Iterator, Tuple

from .reader import ExploreCallable, MoleculeEntry, Reader

__all__ = ["ZipReader"]


class ZipReader(Reader):
    def __init__(self) -> None:
        super().__init__()

    def read(self, input_stream: Any, explore: ExploreCallable) -> Iterator[MoleculeEntry]:
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
                        # the underlying reader only sees the file content as a stream
                        # -> it might believe that the source is "raw_input"
                        # -> we need to correct that here
                        if len(entry.source) == 1 and entry.source[0] == "raw_input":
                            source: Tuple[str, ...] = tuple()
                        else:
                            source = entry.source

                        yield entry._replace(source=(member, *source))

    def __repr__(self) -> str:
        return "ZipReader()"
