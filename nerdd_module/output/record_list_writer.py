from .writer import Writer
from .writer_registry import register_writer

__all__ = ["RecordListWriter"]


@register_writer("record_list")
class RecordListWriter(Writer):
    def __init__(self) -> None:
        pass

    def write(self, records):
        return list(records)
