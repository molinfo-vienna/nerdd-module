from typing import Any, Iterator

from rdkit.Chem import MolFromSmiles

from ..polyfills import BlockLogs
from ..problem import Problem
from .reader import ExploreCallable, MoleculeEntry
from .reader_config import ReaderConfig
from .stream_reader import StreamReader

__all__ = ["SmilesReader"]


class SmilesReader(StreamReader):
    def __init__(self, max_length_smiles: int = 10_000) -> None:
        super().__init__()
        self._max_length_smiles = max_length_smiles

    def _read_stream(self, input_stream: Any, explore: ExploreCallable) -> Iterator[MoleculeEntry]:
        # suppress RDKit warnings
        with BlockLogs():
            for line in input_stream:
                # skip empty lines
                if line.strip() == "":
                    continue

                # skip comments
                if line.strip().startswith("#"):
                    continue

                line = line.strip("\n")

                # avoid long smiles strings, because they might take veeeeery long to parse
                if len(line) > self._max_length_smiles:
                    errors = [
                        Problem(
                            "line_too_long",
                            f"Line exceeds max length of {self._max_length_smiles} characters",
                        )
                    ]
                    yield MoleculeEntry(
                        raw_input=line[: self._max_length_smiles - 3] + "...",
                        input_type="smiles",
                        source=("raw_input",),
                        mol=None,
                        errors=errors,
                    )
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
        return f"SmilesReader(max_length={self._max_length_smiles})"

    config = ReaderConfig(examples=["C1=NC2=C(N1COCCO)N=C(NC2=O)N"])
