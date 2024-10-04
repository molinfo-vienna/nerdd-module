from typing import Any

from .converter import Converter


class IdentityConverter(Converter, data_type=None, output_format=None):
    def _convert(self, input: Any, context: dict, **kwargs: Any) -> dict:
        return input
