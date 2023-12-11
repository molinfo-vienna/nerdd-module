from typing import BinaryIO, Dict, Iterable, TextIO, Union

from rdkit.Chem import Mol, MolToSmiles, SDWriter

from .writer import Writer


class SdfWriter(Writer):
    def __init__(self):
        super().__init__(writes_bytes=False)

    def _output_type(self) -> str:
        return "sdf"

    def _write(self, output, entries: Iterable[Dict]):
        writer = SDWriter(output)
        try:
            for entry in entries:
                # assume that there is a mol object
                mol = entry["input_mol"]

                # write (almost) all properties to the mol object
                for key, value in entry.items():
                    if isinstance(value, Mol):
                        value = MolToSmiles(value)
                    elif isinstance(value, str) and "\n" in value:
                        # SDF can't write multi-line strings
                        continue

                    mol.SetProp(key, str(value))

                # write molecule
                writer.write(mol)
        finally:
            writer.close()
