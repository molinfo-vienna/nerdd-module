import csv
from io import TextIOWrapper
from itertools import chain
from typing import BinaryIO, Dict, Iterable, TextIO, Union

from rdkit.Chem import Mol, MolToSmiles

from .writer import Writer


class CsvWriter(Writer):
    def __init__(self):
        super().__init__()

    def _output_type(self) -> str:
        return "csv"

    def _write(self, output: Union[TextIO, BinaryIO], entries: Iterable[Dict]):
        # CSV writer cannot handle BinaryIO and requires a string stream (~TextIO)
        # --> convert if necessary
        if isinstance(output, BinaryIO):
            encoded_output: TextIO = TextIOWrapper(
                output, encoding="utf-8", write_through=True
            )
        else:
            encoded_output = output

        entry_iter = iter(entries)

        # get the first entry to extract the fieldnames
        first_entry = next(entry_iter)
        writer = csv.DictWriter(encoded_output, fieldnames=first_entry.keys())

        # write header, first entry, and remaining entries
        writer.writeheader()
        for entry in chain([first_entry], entry_iter):
            for key, value in entry.items():
                if isinstance(value, Mol):
                    entry[key] = MolToSmiles(value)
            writer.writerow(entry)
