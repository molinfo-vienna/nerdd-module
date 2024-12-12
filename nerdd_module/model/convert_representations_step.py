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
        self._result_properties = result_properties
        self._converter_map = {
            p.name: Converter.get_converter(p, output_format, **kwargs) for p in result_properties
        }

    def _process(self, record: dict) -> dict:
        result = {
            k.name: self._converter_map[k.name].convert(
                input=record.get(k.name, None), context=record
            )
            for k in self._result_properties
        }

        return {k: v for k, v in result.items() if v is not Converter.HIDE}
