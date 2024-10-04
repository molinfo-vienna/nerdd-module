from typing import IO, Any, Dict, Iterable

from rdkit.Chem import SDWriter

from .file_writer import FileLike, FileWriter

__all__ = ["SdfWriter"]


class SdfWriter(FileWriter, output_format="sdf"):
    def __init__(self, output_file: FileLike) -> None:
        super().__init__(output_file, writes_bytes=False)

    def _write(self, output: IO[Any], entries: Iterable[Dict]) -> None:
        writer = SDWriter(output)
        try:
            for entry in entries:
                # assume that there is a mol object
                mol = entry["input_mol"]

                # write (almost) all properties to the mol object
                for key, value in entry.items():
                    value_as_str = str(value)
                    if "\n" in value_as_str:
                        # SDF can't write multi-line strings
                        continue

                    mol.SetProp(key, value_as_str)

                # write molecule
                writer.write(mol)
        finally:
            writer.close()
