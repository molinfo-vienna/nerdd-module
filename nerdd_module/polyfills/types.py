import sys

__all__ = ["PathLikeStr"]

if sys.version_info < (3, 9):
    from typing_extensions import Protocol

    class PathLikeStr(Protocol):
        def __fspath__(self) -> str: ...

else:
    from os import PathLike

    PathLikeStr = PathLike[str]
