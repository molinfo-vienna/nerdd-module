from typing import Any, Iterator

from rdkit.Chem import MolFromInchi

from ..polyfills import BlockLogs
from ..problem import Problem
from .reader import ExploreCallable, MoleculeEntry
from .reader_config import ReaderConfig
from .stream_reader import StreamReader

__all__ = ["InchiReader"]


class InchiReader(StreamReader):
    def __init__(self) -> None:
        super().__init__()

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

                try:
                    mol = MolFromInchi(line, sanitize=False)
                except:  # noqa: E722 (allow bare except, because RDKit is unpredictable)
                    mol = None

                if mol is None:
                    errors = [Problem("invalid_inchi", "Invalid InChI")]
                else:
                    errors = []

                yield MoleculeEntry(
                    raw_input=line.strip("\n"),
                    input_type="inchi",
                    source=("raw_input",),
                    mol=mol,
                    errors=errors,
                )

    def __repr__(self) -> str:
        return "InchiReader()"

    config = ReaderConfig(
        examples=[
            "InChI=1S/C18H16O3/c1-2-13(12-8-4-3-5-9-12)16-17(19)14-10-6-7-11-15(14)21-18(16)20/h3-11,13,19H,2H2,1H3"
        ]
    )
