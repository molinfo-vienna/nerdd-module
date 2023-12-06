from abc import ABC, abstractmethod
from typing import Dict, List

__all__ = ["Configuration"]


class Configuration(ABC):
    def __init__(self):
        pass

    def get_dict(self) -> Dict:
        config_dict = self._get_dict()

        return config_dict

    @abstractmethod
    def _get_dict(self) -> Dict:
        pass

    def molecular_property_columns(self) -> List[str]:
        return [
            c["name"]
            for c in self.get_dict().get("result_properties", [])
            if "level" not in c or c["level"] == "molecule"
        ]

    def atom_property_columns(self) -> List[str]:
        return [
            c["name"]
            for c in self.get_dict().get("result_properties", [])
            if "level" in c and c["level"] == "atom"
        ]

    def derivative_property_columns(self) -> List[str]:
        return [
            c["name"]
            for c in self.get_dict().get("result_properties", [])
            if "level" in c and c["level"] == "derivative"
        ]

    def get_module_type(self) -> str:
        assert (
            len(self.atom_property_columns()) == 0
            or len(self.derivative_property_columns()) == 0
        ), "A module can only predict atom or derivative properties, not both."

        if len(self.atom_property_columns()) > 0:
            return "atom_property_predictor"
        elif len(self.derivative_property_columns()) > 0:
            return "derivative_property_predictor"
        else:
            return "molecule_property_predictor"
