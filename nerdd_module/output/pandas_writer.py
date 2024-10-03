from typing import Iterable

import pandas as pd

from .writer import Writer

__all__ = ["PandasWriter"]


class PandasWriter(Writer):
    def __init__(self) -> None:
        pass

    def write(self, records: Iterable[dict]) -> pd.DataFrame:
        df = pd.DataFrame(records)
        return df

    @classmethod
    def get_output_format(cls) -> str:
        return "pandas"
