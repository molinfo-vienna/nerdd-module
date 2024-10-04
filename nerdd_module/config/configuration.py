from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Any, List, Union

__all__ = ["Configuration"]


def get_property_columns_of_type(config: dict, t: str) -> List[dict]:
    return [c for c in config["result_properties"] if c.get("level", "molecule") == t]


class Configuration(ABC):
    def __init__(self) -> None:
        pass

    @lru_cache
    def get_dict(self) -> dict:
        config = self._get_dict()

        if "result_properties" not in config:
            config["result_properties"] = []

        # check that a module can only predict atom or derivative properties, not both
        num_atom_properties = len(get_property_columns_of_type(config, "atom"))
        num_derivative_properties = len(
            get_property_columns_of_type(config, "derivative")
        )
        assert (
            num_atom_properties == 0 or num_derivative_properties == 0
        ), "A module can only predict atom or derivative properties, not both."

        return config

    @abstractmethod
    def _get_dict(self) -> dict:
        pass

    def is_empty(self) -> bool:
        return self.get_dict() == {}

    def molecular_property_columns(self) -> List[dict]:
        return get_property_columns_of_type(self.get_dict(), "molecule")

    def atom_property_columns(self) -> List[dict]:
        return get_property_columns_of_type(self.get_dict(), "atom")

    def derivative_property_columns(self) -> List[dict]:
        return get_property_columns_of_type(self.get_dict(), "derivative")

    def get_task(self) -> str:
        # if task is specified in the config, use that
        config = self.get_dict()
        if "task" in config:
            return config["task"]

        # try to derive the task from the result_properties
        num_atom_properties = len(self.atom_property_columns())
        num_derivative_properties = len(self.derivative_property_columns())

        if num_atom_properties > 0:
            return "atom_property_prediction"
        elif num_derivative_properties > 0:
            return "derivative_property_prediction"
        else:
            return "molecular_property_prediction"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._get_dict()})"
