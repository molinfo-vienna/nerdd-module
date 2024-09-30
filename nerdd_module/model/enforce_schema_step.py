from typing import Iterator
from ..config import Configuration

from ..steps import Step


class EnforceSchemaStep(Step):
    def __init__(self, config: Configuration) -> None:
        super().__init__()
        self._properties = [p["name"] for p in config["result_properties"]]

    def _run(self, source: Iterator[dict]) -> Iterator[dict]:
        for record in source:
            yield {k: record.get(k) for k in self._properties}
