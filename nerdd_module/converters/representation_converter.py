from typing import Any

from rdkit.Chem import MolToInchi, MolToSmiles

from ..config import Module, ResultProperty
from .converter import Converter
from .converter_config import ALL, ConverterConfig

__all__ = ["RepresentationConverter"]


class RepresentationConverter(Converter):
    def __init__(
        self,
        module_config: Module,
        result_property: ResultProperty,
        output_format: str,
        **kwargs: Any,
    ) -> None:
        super().__init__(module_config, result_property, output_format, **kwargs)

        representation = result_property.representation or "smiles"
        if representation == "inchi":
            self._serialize = MolToInchi
        elif representation == "smiles":
            self._serialize = MolToSmiles
        else:
            raise ValueError(f"Unsupported representation: {representation}")

    def _convert(self, input: Any, context: dict) -> Any:
        from_property = self.result_property.from_property

        if from_property is None:
            actual_input = input
        else:
            actual_input = context[from_property]

        try:
            representation = self._serialize(actual_input)
        except:  # noqa: E722 (allow bare except, because RDKit is unpredictable)
            representation = None

        return representation

    config = ConverterConfig(
        data_types="representation",
        output_formats=ALL,
    )
