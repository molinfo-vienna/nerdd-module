from ..polyfills import TypedDict

__all__ = ["WriterConfig"]


class WriterConfig(TypedDict, total=False):
    output_format: str
    is_abstract: bool
