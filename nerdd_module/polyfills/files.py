import sys

__all__ = ["files", "Traversable"]

if sys.version_info < (3, 9):
    from importlib_resources import files
    from importlib_resources.abc import Traversable
else:
    from importlib.resources import files
    from importlib.resources.abc import Traversable
