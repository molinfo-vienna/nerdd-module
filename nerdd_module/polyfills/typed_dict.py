import sys

__all__ = ["TypedDict"]

if sys.version_info < (3, 8):
    from typing_extensions import TypedDict
else:
    from typing import TypedDict
