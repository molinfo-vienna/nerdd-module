from typing import Any

from ..converters import Converter
from ..steps import MapStep

__all__ = ["ConvertRepresentationsStep"]


class ConvertRepresentationsStep(MapStep):
    def __init__(self, result_properties: list, output_format: str, **kwargs: Any) -> None:
        super().__init__()
        self._property_type_map = {
            p["name"]: Converter.get_converter(p.get("type"), output_format, **kwargs)
            for p in result_properties
        }

    def _process(self, record: dict) -> dict:
        return {k: self._property_type_map[k].convert(v, record) for k, v in record.items()}
