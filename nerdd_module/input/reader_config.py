from typing import List

from ..polyfills import TypedDict

__all__ = ["ReaderConfig"]


class ReaderConfig(TypedDict):
    examples: List[str]
