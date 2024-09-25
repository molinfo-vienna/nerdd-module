from abc import ABC, abstractmethod
from functools import lru_cache
from typing import List

__all__ = ["Configuration"]


class Configuration(ABC):
    def __init__(self):
        pass

    @lru_cache
    def get_dict(self) -> dict:
        config = self._get_dict()

        # TODO: validate

        return config

    @abstractmethod
    def _get_dict(self) -> dict:
        pass

    def molecular_property_columns(self) -> List[str]:
        return [
            c["name"]
            for c in self["result_properties"]
            if c.get("level", "molecule") == "molecule"
        ]

    def atom_property_columns(self) -> List[str]:
        return [
            c["name"] for c in self["result_properties"] if c.get("level") == "atom"
        ]

    def derivative_property_columns(self) -> List[str]:
        return [
            c["name"]
            for c in self["result_properties"]
            if c.get("level") == "derivative"
        ]

    def get_task(self) -> str:
        num_atom_properties = len(self.atom_property_columns())
        num_derivative_properties = len(self.derivative_property_columns())
        assert (
            num_atom_properties == 0 or num_derivative_properties == 0
        ), "A module can only predict atom or derivative properties, not both."

        if num_atom_properties > 0:
            return "atom_property_prediction"
        elif num_derivative_properties > 0:
            return "derivative_property_prediction"
        else:
            return "molecular_property_prediction"

    def __getitem__(self, key):
        return self.get_dict()[key]

    def __repr__(self):
        return f"{self.__class__.__name__}({self._get_dict()})"
