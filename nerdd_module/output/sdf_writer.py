from typing import IO, Any, Dict, Iterable

from rdkit.Chem import Mol, SDWriter

from .file_writer import FileLike, FileWriter
from .writer_config import WriterConfig

__all__ = ["SdfWriter"]


class SdfWriter(FileWriter):
    def __init__(self, output_file: FileLike) -> None:
        super().__init__(output_file, writes_bytes=False)

    def _write(self, output: IO[Any], entries: Iterable[Dict]) -> None:
        writer = SDWriter(output)
        try:
            for entry in entries:
                # assume that there is a mol object
                mol = entry["input_mol"]

                # if the molecule is erroneous, use an empty molecule
                if mol is None:
                    mol = Mol()

                # write (almost) all properties to the mol object
                for key, value in entry.items():
                    # skip "input_mol" key, because we use it as the main molecule
                    if key == "input_mol":
                        continue

                    value_as_str = str(value)

                    # SDF can't write multi-line strings
                    # -> replace newline with space
                    value_as_str = value_as_str.replace("\n", " ")

                    mol.SetProp(key, value_as_str)

                # write molecule
                writer.write(mol)
        finally:
            writer.close()

    config = WriterConfig(output_format="sdf")
