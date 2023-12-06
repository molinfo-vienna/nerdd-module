import logging
from typing import Generator, List, Optional

from .elementary_reader import ElementaryReader
from .file_reader import FileReader
from .guessing_reader import GuessingReader
from .list_reader import ListReader
from .reader import MoleculeEntry, Reader
from .reader_registry import ReaderRegistry

__all__ = ["guess_and_read"]

logger = logging.getLogger(__name__)


def guess_and_read(
    input,
    input_type: Optional[str] = None,
    readers: Optional[List[Reader]] = None,
    num_test_entries: int = 10,
) -> Generator[MoleculeEntry, None, None]:
    if readers is None:
        # filter readers by input_type (if specified)
        allowed_input_types = ReaderRegistry().supported_input_types
        if input_type is None:
            input_types = allowed_input_types
        else:
            assert input_type in allowed_input_types
            input_types = frozenset([input_type])

        # compose list of possible readers
        file_readers: List[Reader] = [
            reader
            for reader in ReaderRegistry()
            if reader.input_type in input_types and isinstance(reader, FileReader)
        ]

        elementary_readers: List[Reader] = [
            reader
            for reader in ReaderRegistry()
            if reader.input_type in input_types and isinstance(reader, ElementaryReader)
        ]

        list_readers: List[Reader] = [
            ListReader(inner_reader=reader) for reader in elementary_readers
        ]

        readers = [
            *elementary_readers,
            *list_readers,
            ListReader(
                GuessingReader(readers=file_readers, num_test_entries=num_test_entries)
            ),
        ]

    return GuessingReader(readers=readers, num_test_entries=num_test_entries).read(
        input
    )
