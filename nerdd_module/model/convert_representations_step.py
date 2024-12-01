from typing import Any, List

from ..config import ResultProperty
from ..converters import Converter
from ..steps import MapStep

__all__ = ["ConvertRepresentationsStep"]


class ConvertRepresentationsStep(MapStep):
    def __init__(
        self, result_properties: List[ResultProperty], output_format: str, **kwargs: Any
    ) -> None:
        super().__init__()
        self._converter_map = {
            p.name: Converter.get_converter(p, output_format, **kwargs) for p in result_properties
        }

    def _process(self, record: dict) -> dict:
        result = {
            k: self._converter_map[k].convert(input=v, context=record) for k, v in record.items()
        }

        return {k: v for k, v in result.items() if v is not Converter.HIDE}
