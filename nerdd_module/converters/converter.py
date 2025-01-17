from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Tuple, Union

from ..config import Module, ResultProperty
from ..util import call_with_mappings
from .converter_config import ALL, ALL_TYPE

__all__ = ["Converter"]


logger = logging.getLogger(__name__)


_factories: Dict[
    Tuple[Union[str, ALL_TYPE], Union[str, ALL_TYPE]], Callable[[dict], Converter]
] = {}


class Converter(ABC):
    # a special symbol to indicate that a property should be hidden
    HIDE = object()

    def __init__(
        self,
        module_config: Module,
        result_property: ResultProperty,
        output_format: str,
        **kwargs: Any,
    ) -> None:
        super().__init__()
        self.module_config = module_config
        self.result_property = result_property
        self.output_format = output_format

    @classmethod
    def __init_subclass__(
        cls,
        **kwargs: Any,
    ) -> None:
        super().__init_subclass__(**kwargs)

        assert hasattr(
            cls, "config"
        ), "All subclasses of Converter need to have a config attribute of type ConverterConfig"

        data_types = cls.config["data_types"]
        output_formats = cls.config["output_formats"]
        is_abstract = cls.config.get("is_abstract", False)

        if not is_abstract:
            if isinstance(data_types, str) or data_types is ALL:
                data_types_list = [data_types]
            else:
                data_types_list = data_types

            if isinstance(output_formats, str) or output_formats is ALL:
                output_formats_list = [output_formats]
            else:
                output_formats_list = output_formats

            for output_format in output_formats_list:
                for data_type in data_types_list:
                    logger.debug(f"Registering converter {cls} for {data_type} -> {output_format}")
                    _factories[(data_type, output_format)] = cls

    @abstractmethod
    def _convert(self, input: Any, context: dict) -> Any:
        pass

    def convert(self, input: Any, context: dict) -> Any:
        return self._convert(input, context)

    @classmethod
    def get_converter(
        cls,
        module_config: Module,
        result_property: ResultProperty,
        output_format: str,
        return_default: bool = True,
        **kwargs: Any,
    ) -> Converter:
        data_type = result_property.type
        if (data_type, output_format) not in _factories:
            ConverterFunc = None
            if return_default:
                if (data_type, ALL) in _factories:
                    ConverterFunc = _factories[(data_type, ALL)]
                elif (ALL, output_format) in _factories:
                    ConverterFunc = _factories[(ALL, output_format)]
                elif (ALL, ALL) in _factories:
                    ConverterFunc = _factories[(ALL, ALL)]

            if ConverterFunc is None:
                raise ValueError(
                    f"Unknown data type '{data_type}' or output format '{output_format}'"
                )
        else:
            ConverterFunc = _factories[(data_type, output_format)]

        # kwargs will be passed to the constructor of the converter
        # --> add data_type and output_format to the kwargs
        kwargs["module_config"] = module_config
        kwargs["result_property"] = result_property
        kwargs["output_format"] = output_format

        return call_with_mappings(ConverterFunc, kwargs)
