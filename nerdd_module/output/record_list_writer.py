from typing import Iterable, List

from .writer import Writer

__all__ = ["RecordListWriter"]


class RecordListWriter(Writer, output_format="record_list"):
    def __init__(self) -> None:
        pass

    def write(self, records: Iterable[dict]) -> List[dict]:
        return list(records)
