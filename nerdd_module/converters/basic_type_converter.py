from typing import Any, Callable

from ..config import Module, ResultProperty
from .converter import Converter
from .converter_config import ALL, ConverterConfig

__all__ = ["BasicTypeConverter", "basic_data_types"]

basic_data_types = [
    "integer",
    "int",
    "float",
    "string",
    "str",
    "boolean",
    "bool",
]


class BasicTypeConverter(Converter):
    def __init__(
        self,
        module_config: Module,
        result_property: ResultProperty,
        output_format: str,
        **kwargs: Any,
    ) -> None:
        super().__init__(module_config, result_property, output_format, **kwargs)
        self.type = self.result_property.type

        self._f: Callable[[Any], Any]
        if self.type == "integer" or self.type == "int":
            self._f = int
        elif self.type == "float":
            self._f = float
        elif self.type == "string" or self.type == "str":
            self._f = str
        elif self.type == "boolean" or self.type == "bool":
            self._f = bool
        else:
            self._f = lambda v: v

    def _convert(self, input: Any, context: dict) -> Any:
        if input is None:
            return None

        return self._f(input)

    config = ConverterConfig(
        data_types=basic_data_types,
        output_formats=ALL,
    )
