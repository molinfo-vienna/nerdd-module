import sys

__all__ = ["version"]

if sys.version_info < (3, 10):
    from importlib_metadata import version
else:
    from importlib.metadata import version
