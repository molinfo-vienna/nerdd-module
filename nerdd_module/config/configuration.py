from abc import ABC, abstractmethod
from functools import lru_cache
from typing import List

__all__ = ["Configuration"]


def get_property_columns_of_type(config: dict, t: str) -> List[dict]:
    return [c for c in config["result_properties"] if c.get("level", "molecule") == t]


def is_visible(result_property: dict, output_format: str) -> bool:
    formats = result_property.get("formats", {})

    if isinstance(formats, list):
        return output_format in formats
    elif isinstance(formats, dict):
        include = formats.get("include", "*")
        exclude = formats.get("exclude", [])
        assert include == "*" or isinstance(
            include, list
        ), f"Expected include to be a list or '*', got {include}"
        assert isinstance(exclude, list), f"Expected exclude to be a list, got {exclude}"
        return (include == "*" or output_format in include) and output_format not in exclude
    else:
        raise ValueError(
            f"Invalid formats declaration {formats} in result property " f"{result_property}"
        )


class Configuration(ABC):
    def __init__(self) -> None:
        pass

    @lru_cache(1)
    def get_dict(self) -> dict:
        config = self._get_dict()

        if "result_properties" not in config:
            config["result_properties"] = []

        # check that a module can only predict atom or derivative properties, not both
        num_atom_properties = len(get_property_columns_of_type(config, "atom"))
        num_derivative_properties = len(get_property_columns_of_type(config, "derivative"))
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

    def get_visible_properties(self, output_format: str) -> List[dict]:
        return [
            p for p in self.get_dict().get("result_properties", []) if is_visible(p, output_format)
        ]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._get_dict()})"
