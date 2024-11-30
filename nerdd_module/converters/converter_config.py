from typing import List, Optional, Union

from ..polyfills import Literal, TypedDict

__all__ = ["ConverterConfig", "ALL", "ALL_TYPE"]


# a special symbol to indicate that all data types / output formats are considered
ALL_TYPE = Literal["ALL"]
ALL: ALL_TYPE = "ALL"


class ConverterConfig(TypedDict):
    data_types: Optional[Union[str, List[str], ALL_TYPE]]
    output_formats: Optional[Union[str, List[str], ALL_TYPE]]
