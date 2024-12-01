from typing import Any

from rdkit.Chem import MolToInchi, MolToSmiles

from ..config import ResultProperty
from .converter import Converter
from .converter_config import ALL, ConverterConfig

__all__ = ["MolConverter"]


class MolConverter(Converter):
    def __init__(self, result_property: ResultProperty, output_format: str, **kwargs: Any) -> None:
        super().__init__(result_property, output_format, **kwargs)

        if output_format == "sdf" and result_property.name == "input_mol":
            # in an SDF, the main molecule (input_mol) can be a Mol object
            self._serialize = lambda x: x
        elif output_format in ["pandas", "record_list", "iterator"]:
            self._serialize = lambda mol: mol
        else:
            representation = result_property.representation or "smiles"
            if representation == "inchi":
                self._serialize = MolToInchi
            elif representation == "smiles":
                self._serialize = MolToSmiles
            else:
                raise ValueError(f"Unsupported representation: {representation}")

    def _convert(self, input: Any, context: dict) -> Any:
        try:
            representation = self._serialize(input)
        except:  # noqa: E722 (allow bare except, because RDKit is unpredictable)
            representation = None

        return representation

    config = ConverterConfig(
        data_types="mol",
        output_formats=ALL,
    )
