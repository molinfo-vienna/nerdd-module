import sys
from typing import Iterable

from typing_extensions import Protocol


class EntryPoint(Protocol):
    def load(self) -> None: ...


__all__ = ["get_entry_points"]

# import entry_points from importlib.metadata or fall back to pkg_resources
try:
    if sys.version_info < (3, 10):
        from importlib_metadata import entry_points
    else:
        from importlib.metadata import entry_points

    def get_entry_points(group: str) -> Iterable[EntryPoint]:
        return entry_points(group=group)

except ImportError:
    import pkg_resources

    def get_entry_points(group: str) -> Iterable[EntryPoint]:
        return pkg_resources.iter_entry_points(group)
