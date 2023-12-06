try:
    # Try to use the standard library version first (Python 3.8+).
    from importlib.metadata import version
except ImportError:
    # If that fails, use the backport for Python 3.7.
    from importlib_metadata import version

__all__ = ["__version__"]

__version__ = version("nerdd-module")
