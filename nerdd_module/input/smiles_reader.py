from codecs import getreader
from typing import Any, Iterator

from rdkit.Chem import MolFromSmiles
from rdkit.rdBase import BlockLogs

from ..problem import Problem
from .reader import ExploreCallable, MoleculeEntry, Reader
from .reader_config import ReaderConfig

__all__ = ["SmilesReader"]

StreamReader = getreader("utf-8")


class SmilesReader(Reader):
    def __init__(self) -> None:
        super().__init__()

    def read(self, input_stream: Any, explore: ExploreCallable) -> Iterator[MoleculeEntry]:
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
                except:  # noqa: E722 (allow bare except, because RDKit is unpredictable)
                    mol = None

                if mol is None:
                    display_line = line
                    if len(display_line) > 100:
                        display_line = display_line[:100] + "..."
                    errors = [Problem("invalid_smiles", f"Invalid SMILES {display_line}")]
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
                    source=("raw_input",),
                    mol=mol,
                    errors=errors,
                )

    def __repr__(self) -> str:
        return "SmilesReader()"

    config = ReaderConfig(examples=["C1=NC2=C(N1COCCO)N=C(NC2=O)N"])
