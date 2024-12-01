from typing import Any

from .converter import Converter
from .converter_config import ALL, ConverterConfig

__all__ = ["VoidConverter"]


class VoidConverter(Converter):
    def _convert(self, input: Any, context: dict) -> Any:
        return Converter.HIDE

    # by default, all data types will be hidden for all output formats
    config = ConverterConfig(
        data_types=ALL,
        output_formats=ALL,
    )
