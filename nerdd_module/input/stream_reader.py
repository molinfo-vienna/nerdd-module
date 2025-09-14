from abc import abstractmethod
from codecs import getreader
from typing import Any, Iterator, Optional

import chardet

from .reader import ExploreCallable, MoleculeEntry, Reader

__all__ = ["StreamReader"]


class StreamReader(Reader):
    def __init__(self, encoding: Optional[str] = "utf-8-sig") -> None:
        super().__init__()
        self.encoding = encoding

    def read(self, input_stream: Any, explore: ExploreCallable) -> Iterator[MoleculeEntry]:
        if not hasattr(input_stream, "read") or not hasattr(input_stream, "seek"):
            raise TypeError("input must be a stream-like object")

        input_stream.seek(0)

        #
        # detect file encoding (if not provided)
        #

        # read a portion of the file's content
        if self.encoding is None:
            sample = input_stream.read(1_000_000)
            result = chardet.detect(sample)
            if result["confidence"] > 0.5 and result["encoding"] is not None:
                encoding = result["encoding"]
            else:
                encoding = "utf-8-sig"

            input_stream.seek(0)
        else:
            encoding = self.encoding

        #
        # read file
        #
        StreamReader = getreader(encoding)
        # errors="replace": replace invalid characters instead of failing
        reader = StreamReader(input_stream, "replace")
        return self._read_stream(reader, explore)

    @abstractmethod
    def _read_stream(self, input_stream: Any, explore: ExploreCallable) -> Iterator[MoleculeEntry]:
        pass
