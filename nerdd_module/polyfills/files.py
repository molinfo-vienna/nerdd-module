import sys

__all__ = ["files", "Traversable", "as_file"]

if sys.version_info < (3, 9):
    from importlib_resources import as_file, files
    from importlib_resources.abc import Traversable
else:
    try:
        from importlib.abc import Traversable
    except ImportError:
        from importlib.resources.abc import Traversable
    from importlib.resources import as_file, files
