import logging
from typing import BinaryIO, Generator, List

from .reader import MoleculeEntry, Reader

logger = logging.getLogger(__name__)

__all__ = ["GuessingReader"]


class GuessingReader(Reader):
    def __init__(self, readers: List[Reader], num_test_entries: int = 10):
        super().__init__()
        assert len(readers) > 0
        assert num_test_entries > 0
        self.readers = readers
        self.num_test_entries = num_test_entries

    def read(self, input) -> Generator[MoleculeEntry, None, None]:
        logger.info("Guessing the input type")

        # try all readers and take a sample of the first num_test_entries
        # the reader with most valid molecule entries will be used
        def test_reader(reader: Reader) -> int:
            logger.info(f"Attempting to use {reader.__class__.__name__}")
            try:
                result = [
                    entry
                    for entry, _ in zip(
                        reader.read(input), range(self.num_test_entries)
                    )
                ]
                valid_entries = [
                    entry
                    for entry in result
                    if entry is not None and entry.mol is not None
                ]
                return len(valid_entries)
            except Exception as e:
                logger.info(f"Failed to use the reader; reason: {e}")
                return -1

        reader_scores = [(reader, test_reader(reader)) for reader in self.readers]
        best_reader, best_score = max(reader_scores, key=lambda x: x[1])

        # TODO: add a threshold for the score

        logger.info(f"Using {best_reader.__class__.__name__}")
        yield from best_reader.read(input)

    def _input_type(self) -> str:
        return "unknown"
