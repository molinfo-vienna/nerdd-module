from os import PathLike
from pathlib import Path
from typing import Iterator, Optional, Tuple, Union

from .reader import MoleculeEntry, Reader
from .reader_registry import register_reader

__all__ = ["FileReader"]


@register_reader
class FileReader(Reader):
    def __init__(self, data_dir: Union[str, PathLike, None] = None):
        super().__init__()
        self.data_dir = data_dir
        if self.data_dir is not None:
            self.data_dir = Path(self.data_dir)

    def read(self, filename, explore) -> Iterator[MoleculeEntry]:
        assert isinstance(filename, str), "input must be a string"

        # convert filename to path
        try:
            path = Path(filename)
        except:
            raise ValueError("input must be a valid path")

        # convert to absolute path
        if not path.is_absolute():
            if self.data_dir is not None:
                path = self.data_dir / path
            else:
                path = Path(".") / path

        # check that the file is within the data_dir
        assert (
            self.data_dir is None or self.data_dir in path.parents
        ), "input must be a relative path"

        # check that the file exists
        assert path.exists(), "input must be a valid file"

        with open(path, "rb") as f:
            for entry in explore(f):
                if len(entry.source) == 1 and entry.source[0] == "raw_input":
                    source: Tuple[str, ...] = tuple()
                else:
                    source = entry.source
                yield entry._replace(source=tuple([filename, *source]))

    def __repr__(self):
        return f"FileReader()"
