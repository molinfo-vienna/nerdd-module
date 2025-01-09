import logging
from typing import Any

from .converter import Converter
from .converter_config import ConverterConfig

__all__ = ["SourceListIdentityConverter", "SourceListConverter"]

logger = logging.getLogger(__name__)


class SourceListIdentityConverter(Converter):
    def _convert(self, input: Any, context: dict) -> Any:
        return input

    config = ConverterConfig(
        data_types="source_list",
        output_formats=["pandas", "iterator", "record_list"],
    )


class SourceListConverter(Converter):
    def _convert(self, input: Any, context: dict) -> Any:
        return " / ".join(source for source in input)

    config = ConverterConfig(
        data_types="source_list",
        output_formats=["csv", "sdf"],
    )
