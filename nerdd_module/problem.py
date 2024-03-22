from typing import NamedTuple

__all__ = ["Problem"]


class Problem(NamedTuple):
    type: str
    message: str
