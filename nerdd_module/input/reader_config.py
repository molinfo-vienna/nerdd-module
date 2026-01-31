from typing import List

from ..polyfills import TypedDict

__all__ = ["ReaderConfig"]


class ReaderConfig(TypedDict, total=False):
    input_format: str
    examples: List[str]
