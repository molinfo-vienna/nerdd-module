from os import PathLike
from pathlib import Path
from typing import Any, Iterator, Tuple, Union

from .reader import ExploreCallable, MoleculeEntry, Reader
from .reader_config import ReaderConfig

__all__ = ["FileReader"]


class FileReader(Reader):
    def __init__(
        self,
        data_dir: Union[str, PathLike, None] = Path("."),
        allow_paths_outside_data_dir: bool = True,
    ) -> None:
        super().__init__()
        self.data_dir = Path(data_dir).resolve() if data_dir is not None else None
        self.allow_paths_outside_data_dir = allow_paths_outside_data_dir

    def read(self, filename: Any, explore: ExploreCallable) -> Iterator[MoleculeEntry]:
        data_dir = self.data_dir
        if data_dir is None:
            raise PermissionError("file system access is disabled")

        assert isinstance(filename, (str, bytes)), "input must be a string or bytes"

        if isinstance(filename, bytes):
            filename_str = filename.decode("utf-8")
        else:
            filename_str = filename

        # convert filename to path
        try:
            path = Path(filename_str)
        except TypeError as e:
            raise ValueError("input must be a valid path") from e

        # Resolve relative paths against data_dir and canonicalize both relative and absolute paths.
        if not path.is_absolute():
            path = data_dir / path
        path = path.resolve()

        if not self.allow_paths_outside_data_dir and not path.is_relative_to(data_dir):
            raise PermissionError("input path must be within data_dir")

        # check that the file exists
        assert path.exists(), "input must be a valid file"

        with open(path, "rb") as f:
            for entry in explore(f):
                if len(entry.source) == 1 and entry.source[0] == "raw_input":
                    source: Tuple[str, ...] = tuple()
                else:
                    source = entry.source
                yield entry._replace(source=(filename_str, *source))

    def __repr__(self) -> str:
        return (
            f"FileReader(data_dir={self.data_dir}, "
            f"allow_paths_outside_data_dir={self.allow_paths_outside_data_dir})"
        )

    config = ReaderConfig(examples=["compounds.smiles"])
