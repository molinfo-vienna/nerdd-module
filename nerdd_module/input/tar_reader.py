import tarfile
from typing import Any, Iterator, Tuple

from ..problem import Problem
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

                try:
                    for entry in explore(tar.extractfile(member)):
                        # the underlying reader only sees the file content as a stream
                        # -> it might believe that the source is "raw_input"
                        # -> we need to correct that here
                        if len(entry.source) == 1 and entry.source[0] == "raw_input":
                            source: Tuple[str, ...] = tuple()
                        else:
                            source = entry.source
                        yield entry._replace(source=(member.name, *source))
                except Exception as e:
                    yield MoleculeEntry(
                        raw_input="<tar>",
                        input_type="unknown",
                        source=(member.name,),
                        mol=None,
                        errors=[
                            Problem(
                                "invalid_tar_member",
                                f"Could not read tar member '{member.name}': {e}",
                            )
                        ],
                    )

    def __repr__(self) -> str:
        return "TarReader()"
