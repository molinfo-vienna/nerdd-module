from typing import Iterable, List

from .writer import Writer
from .writer_config import WriterConfig

__all__ = ["RecordListWriter"]


class RecordListWriter(Writer):
    def __init__(self) -> None:
        pass

    def write(self, records: Iterable[dict]) -> List[dict]:
        return list(records)

    config = WriterConfig(output_format="record_list")
