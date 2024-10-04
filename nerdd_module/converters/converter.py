from __future__ import annotations

from abc import ABC, abstractmethod
from functools import partial
from typing import Any, Callable, Dict, Optional, Tuple

from ..util import call_with_mappings

__all__ = ["Converter"]


_factories: Dict[Tuple[Optional[str], Optional[str]], Callable[[dict], Converter]] = {}


class Converter(ABC):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def __init_subclass__(
        cls,
        output_format: Optional[str] = None,
        data_type: Optional[str] = None,
        is_abstract: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init_subclass__(**kwargs)
        if not is_abstract:
            _factories[(data_type, output_format)] = partial(call_with_mappings, cls)

    @abstractmethod
    def _convert(self, input: Any, context: dict, **kwargs: Any) -> Any:
        pass

    def convert(self, input: Any, context: dict, **kwargs: Any) -> Any:
        return self._convert(input, context, **kwargs)

    @classmethod
    def get_converter(
        cls,
        data_type: str,
        output_format: str,
        return_default: bool = True,
        **kwargs: Any,
    ) -> Converter:
        if (data_type, output_format) not in _factories:
            default = None
            if return_default:
                if (data_type, None) in _factories:
                    default = _factories[(data_type, None)]
                elif (None, output_format) in _factories:
                    default = _factories[(None, output_format)]
                elif (None, None) in _factories:
                    default = _factories[(None, None)]

            if default is None:
                raise ValueError(
                    f"Unknown data type '{data_type}' or output format '{output_format}'"
                )
            return default(kwargs)

        return _factories[(data_type, output_format)](kwargs)
