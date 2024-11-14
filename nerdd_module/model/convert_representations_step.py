from typing import Any

from ..converters import Converter
from ..steps import MapStep

__all__ = ["ConvertRepresentationsStep"]


class ConvertRepresentationsStep(MapStep):
    def __init__(self, result_properties: list, output_format: str, **kwargs: Any) -> None:
        super().__init__()
        self._converter_map = {
            p.name: Converter.get_converter(p.type, output_format, property=p, **kwargs)
            for p in result_properties
        }

    def _process(self, record: dict) -> dict:
        return {
            k: self._converter_map[k].convert(input=v, context=record) for k, v in record.items()
        }
