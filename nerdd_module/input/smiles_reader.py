from codecs import getreader
from typing import Generator

from rdkit.Chem import MolFromSmiles
from rdkit.rdBase import BlockLogs

from ..problem import Problem
from .reader import MoleculeEntry, Reader
from .reader_registry import register_reader

__all__ = ["SmilesReader"]

StreamReader = getreader("utf-8")


@register_reader
class SmilesReader(Reader):
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
                    mol = MolFromSmiles(line, sanitize=False)
                except:
                    mol = None

                if mol is None:
                    errors = [Problem("invalid_smiles", "Invalid SMILES")]
                else:
                    # old versions of RDKit do not parse the name
                    # --> get name from smiles manually
                    if not mol.HasProp("_Name"):
                        parts = line.split(maxsplit=1)
                        if len(parts) > 1:
                            mol.SetProp("_Name", parts[1])

                    errors = []

                yield MoleculeEntry(
                    raw_input=line,
                    input_type="smiles",
                    source=tuple(["raw_input"]),
                    mol=mol,
                    errors=errors,
                )

    def __repr__(self) -> str:
        return "SmilesReader()"
