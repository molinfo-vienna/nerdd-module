from typing import Iterable

import pandas as pd

from .writer import Writer
from .writer_config import WriterConfig

__all__ = ["PandasWriter"]


class PandasWriter(Writer):
    def __init__(self) -> None:
        pass

    def write(self, records: Iterable[dict]) -> pd.DataFrame:
        df = pd.DataFrame(records)
        return df

    config = WriterConfig(output_format="pandas")
