from typing import Iterable

from typing_extensions import Protocol


class EntryPoint(Protocol):
    def load(self) -> None: ...


__all__ = ["get_entry_points"]

# import entry_points from importlib.metadata or fall back to pkg_resources
# TODO: add importlib_metadata as another option
try:
    from importlib.metadata import entry_points

    def get_entry_points(group: str) -> Iterable[EntryPoint]:
        return entry_points(group=group)
        # TODO: check when this happens:
        # try:
        #     return entry_points(group=group)
        # except TypeError:
        #     return entry_points().get(group, [])

except ImportError:
    import pkg_resources

    def get_entry_points(group: str) -> Iterable[EntryPoint]:
        return pkg_resources.iter_entry_points(group)
