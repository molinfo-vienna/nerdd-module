import sys

__all__ = ["files", "Traversable", "as_file"]

if sys.version_info < (3, 9):
    from importlib_resources import as_file, files
    from importlib_resources.abc import Traversable
else:
    if sys.version_info < (3, 11):
        from importlib.abc import Traversable
    else:
        from importlib.resources.abc import Traversable
    from importlib.resources import as_file, files
