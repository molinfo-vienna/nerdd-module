import csv
from io import TextIOWrapper
from itertools import chain
from typing import BinaryIO, Dict, Iterable, TextIO, Union

from rdkit.Chem import Mol, MolToSmiles

from .writer import Writer


class CsvWriter(Writer):
    def __init__(self):
        super().__init__(writes_bytes=False)

    def _output_type(self) -> str:
        return "csv"

    def _write(self, output, entries: Iterable[Dict]):
        entry_iter = iter(entries)

        # get the first entry to extract the fieldnames
        first_entry = next(entry_iter)
        writer = csv.DictWriter(output, fieldnames=first_entry.keys())

        # write header, first entry, and remaining entries
        writer.writeheader()
        for entry in chain([first_entry], entry_iter):
            for key, value in entry.items():
                if isinstance(value, Mol):
                    entry[key] = MolToSmiles(value)
            writer.writerow(entry)
