from typing import Any

from .converter import Converter
from .converter_config import ConverterConfig

__all__ = ["MolConverter"]


class MolConverter(Converter):
    def _convert(self, input: Any, context: dict) -> Any:
        if self.output_format == "sdf" and self.result_property.name != "input_mol":
            # in an SDF, the main molecule (input_mol) can be a Mol object
            return Converter.HIDE
        elif self.output_format in ["sdf", "pandas", "record_list", "iterator"]:
            return input

    config = ConverterConfig(
        data_types="mol",
        output_formats=["sdf", "pandas", "record_list", "iterator"],
    )
