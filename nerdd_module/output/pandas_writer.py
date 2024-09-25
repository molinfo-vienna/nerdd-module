import pandas as pd

from .writer import Writer
from .writer_registry import register_writer

__all__ = ["PandasWriter"]


@register_writer("pandas")
class PandasWriter(Writer):
    def __init__(self) -> None:
        pass

    def write(self, records):
        df = pd.DataFrame(records)
        return df
