import sys

__all__ = ["Literal"]

if sys.version_info < (3, 8):
    from typing_extensions import Literal
else:
    from typing import Literal
