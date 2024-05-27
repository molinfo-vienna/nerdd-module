from codecs import getreader
from typing import Generator

from rdkit.Chem import MolFromInchi
from rdkit.rdBase import BlockLogs

from ..problem import Problem
from .reader import MoleculeEntry, Reader
from .reader_registry import register_reader

__all__ = ["InchiReader"]

StreamReader = getreader("utf-8")


@register_reader
class InchiReader(Reader):
    def __init__(self):
        super().__init__()

    def read(self, input_stream, explore) -> Generator[MoleculeEntry, None, None]:
        if not hasattr(input_stream, "read") or not hasattr(input_stream, "seek"):
            raise TypeError("input must be a stream-like object")

        input_stream.seek(0)

        reader = StreamReader(input_stream)

        # suppress RDKit warnings
        with BlockLogs():
            for line in reader:
                # skip empty lines
                if line.strip() == "":
                    continue

                # skip comments
                if line.strip().startswith("#"):
                    continue

                try:
                    mol = MolFromInchi(line, sanitize=False)
                except:
                    mol = None

                if mol is None:
                    errors = [Problem("invalid_inchi", "Invalid InChI")]
                else:
                    errors = []

                yield MoleculeEntry(
                    raw_input=line,
                    input_type="inchi",
                    source=tuple(["raw_input"]),
                    mol=mol,
                    errors=errors,
                )

    def __repr__(self) -> str:
        return "InchiReader()"
