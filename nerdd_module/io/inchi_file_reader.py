from codecs import getreader
from typing import BinaryIO, Generator

from .file_reader import FileReader
from .inchi_reader import InchiReader

__all__ = ["InchiFileReader"]

StreamReader = getreader("utf-8")


class InchiFileReader(FileReader):
    def __init__(self):
        super().__init__(InchiReader())

    def _split(self, f: BinaryIO) -> Generator[str, None, None]:
        reader = StreamReader(f)
        for line in reader:
            # skip empty lines
            if line.strip() == "":
                continue

            # skip comments
            if line.strip().startswith("#"):
                continue

            yield line
