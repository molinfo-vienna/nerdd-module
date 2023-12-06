from functools import lru_cache

from .csv_writer import CsvWriter
from .sdf_writer import SdfWriter
from .writer import Writer

__all__ = ["WriterRegistry"]


# lru_cache makes the registry a singleton
@lru_cache(maxsize=1)
class WriterRegistry:
    def __init__(self):
        self._writers = []

    def register(self, writer: Writer):
        self._writers.append(writer)

    def get_writer(self, output_type: str) -> Writer:
        for writer in self._writers:
            if writer.output_type == output_type:
                return writer

        raise ValueError(f"Unsupported output type: {output_type}")

    @property
    def supported_formats(self) -> frozenset:
        return frozenset([writer.output_type for writer in self._writers])

    @property
    def writers(self):
        return frozenset(self._writers)

    def __iter__(self):
        return iter(self._writers)


registry = WriterRegistry()
registry.register(CsvWriter())
registry.register(SdfWriter())
