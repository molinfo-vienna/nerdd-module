from typing import Any

from .converter import Converter
from .converter_config import ALL, ConverterConfig

__all__ = ["BasicTypeConverter", "basic_data_types"]

basic_data_types = [
    "int",
    "float",
    "string",
    "bool",
]


class BasicTypeConverter(Converter):
    def _convert(self, input: Any, context: dict) -> Any:
        return input

    config = ConverterConfig(
        data_types=basic_data_types,
        output_formats=ALL,
    )
