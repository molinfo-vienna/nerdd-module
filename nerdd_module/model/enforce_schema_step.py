import logging
from typing import Iterator

from ..config import Module
from ..steps import Step

__all__ = ["EnforceSchemaStep"]

logger = logging.getLogger(__name__)


class EnforceSchemaStep(Step):
    def __init__(self, config: Module, output_format: str) -> None:
        super().__init__()
        self._property_names = [p.name for p in config.get_visible_properties(output_format)]

        # check that properties are unique
        if len(self._property_names) != len(set(self._property_names)):
            duplicate_properties = {
                x for x in self._property_names if self._property_names.count(x) > 1
            }
            logger.warning(
                f"Duplicate properties in result_properties: {', '.join(duplicate_properties)}"
            )

    def _run(self, source: Iterator[dict]) -> Iterator[dict]:
        for record in source:
            yield {k: record.get(k) for k in self._property_names}
