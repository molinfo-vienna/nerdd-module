from .writer import Writer
from .writer_registry import register_writer

__all__ = ["IteratorWriter"]


@register_writer("iterator")
class IteratorWriter(Writer):
    def __init__(self) -> None:
        pass

    def write(self, records):
        return records
