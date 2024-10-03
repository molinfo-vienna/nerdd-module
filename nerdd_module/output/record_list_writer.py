from typing import Iterable, List

from .writer import Writer

__all__ = ["RecordListWriter"]


class RecordListWriter(Writer):
    def __init__(self) -> None:
        pass

    def write(self, records: Iterable[dict]) -> List[dict]:
        return list(records)

    @classmethod
    def get_output_format(cls) -> str:
        return "record_list"
