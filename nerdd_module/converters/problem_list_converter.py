import logging
from typing import Any, List, Union, cast

from ..problem import Problem
from .converter import Converter
from .converter_config import ALL, ConverterConfig

__all__ = ["ProblemListConverter"]

logger = logging.getLogger(__name__)


class ProblemListConverter(Converter):
    def _convert(self, input: Any, context: dict) -> Any:
        if self.output_format in ["pandas", "iterator", "record_list"]:
            return input
        else:
            problem_list: List[Union[Problem, str]] = cast(List[Union[Problem, str]], input)

            def _represent(problem: Union[Problem, str]) -> str:
                if isinstance(problem, Problem):
                    return f"{problem.type}: {problem.message}"
                else:
                    logger.warning("Item is not an instance of Problem: %s", problem)
                    return problem

            return "; ".join([_represent(problem) for problem in problem_list])

    config = ConverterConfig(
        data_types="problem_list",
        output_formats=ALL,
    )
