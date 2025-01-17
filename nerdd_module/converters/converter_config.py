from typing import List, Union

from ..polyfills import Literal, TypedDict

__all__ = ["ConverterConfig", "ALL", "ALL_TYPE"]


# a special symbol to indicate that all data types / output formats are considered
ALL_TYPE = Literal["ALL"]
ALL: ALL_TYPE = "ALL"


class ConverterConfig(TypedDict, total=False):
    data_types: Union[str, List[str], ALL_TYPE]
    output_formats: Union[str, List[str], ALL_TYPE]
    is_abstract: bool
