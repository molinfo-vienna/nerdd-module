from typing import List, TypedDict

__all__ = ["ReaderConfig"]


class ReaderConfig(TypedDict):
    examples: List[str]
