import csv
from itertools import chain
from typing import IO, Any, Dict, Iterable

from .file_writer import FileLike, FileWriter

__all__ = ["CsvWriter"]


class CsvWriter(FileWriter, output_format="csv"):
    def __init__(self, output_file: FileLike) -> None:
        super().__init__(output_file, writes_bytes=False)

    def _write(self, output: IO[Any], entries: Iterable[Dict]) -> None:
        entry_iter = iter(entries)

        # get the first entry to extract the fieldnames
        first_entry = next(entry_iter)
        writer = csv.DictWriter(output, fieldnames=first_entry.keys())

        # write header, first entry, and remaining entries
        writer.writeheader()
        for entry in chain([first_entry], entry_iter):
            writer.writerow(entry)
