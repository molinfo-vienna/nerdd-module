from abc import abstractmethod
from codecs import getreader
from typing import Any, Iterator

import chardet

from .reader import ExploreCallable, MoleculeEntry, Reader

__all__ = ["StreamReader"]


class StreamReader(Reader):
    def __init__(self) -> None:
        super().__init__()

    def read(self, input_stream: Any, explore: ExploreCallable) -> Iterator[MoleculeEntry]:
        if not hasattr(input_stream, "read") or not hasattr(input_stream, "seek"):
            raise TypeError("input must be a stream-like object")

        input_stream.seek(0)

        #
        # detect file encoding
        #

        # read a portion of the file's content
        sample = input_stream.read(1_000_000)
        result = chardet.detect(sample)
        if result["confidence"] > 0.5 and result["encoding"] is not None:
            encoding = result["encoding"]
        else:
            encoding = "utf-8"

        input_stream.seek(0)

        #
        # read file
        #
        StreamReader = getreader(encoding)
        reader = StreamReader(input_stream)
        return self._read_stream(reader, explore)

    @abstractmethod
    def _read_stream(self, input_stream: Any, explore: ExploreCallable) -> Iterator[MoleculeEntry]:
        pass
