from typing import Any

from ..config import Module
from ..converters import Converter
from ..steps import MapStep

__all__ = ["ConvertRepresentationsStep"]


class ConvertRepresentationsStep(MapStep):
    def __init__(self, config: Module, output_format: str, **kwargs: Any) -> None:
        super().__init__()
        self._converters = [
            (p.name, Converter.get_converter(config, p, output_format, **kwargs))
            for p in config.result_properties
        ]

    def _process(self, record: dict) -> dict:
        # convert all properties in record
        result = {
            name: converter.convert(input=record.get(name, None), context=record)
            for (name, converter) in self._converters
        }

        # hide all properties that are marked as hidden
        return {k: v for k, v in result.items() if v is not Converter.HIDE}
