from typing import Any, List, cast

from ..problem import Problem
from .converter import Converter
from .converter_config import ALL, ConverterConfig

__all__ = ["ProblemListConverter"]


class ProblemListConverter(Converter):
    def _convert(self, input: Any, context: dict) -> Any:
        if self.output_format in ["pandas", "iterator", "record_list"]:
            return input
        else:
            problem_list: List[Problem] = cast(List[Problem], input)
            return "; ".join([f"{problem.type}: {problem.message}" for problem in problem_list])

    config = ConverterConfig(
        data_types="problem_list",
        output_formats=ALL,
    )
