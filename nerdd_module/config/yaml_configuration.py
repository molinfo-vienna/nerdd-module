import base64
import mimetypes
import os
from pathlib import Path
from typing import IO, Any, Union

import filetype  # type: ignore
import yaml
from typing_extensions import Protocol

from ..polyfills import PathLikeStr, Traversable, as_file
from .configuration import Configuration

__all__ = ["YamlConfiguration"]


class CustomLoaderLike(Protocol):
    base_path: Union[str, PathLikeStr, Traversable]

    def construct_scalar(self, node: yaml.ScalarNode) -> str: ...


def image_constructor(loader: CustomLoaderLike, node: yaml.Node) -> str:
    assert isinstance(node, yaml.ScalarNode)

    base_path = loader.base_path
    if isinstance(base_path, Traversable):
        pass
    else:
        base_path = Path(base_path)

    # obtain the actual file path from the scalar string node
    filepath = loader.construct_scalar(node)

    p = base_path / filepath

    assert p.is_file(), f"File {p} does not exist"

    # load the image from the provided logo path and convert it to base64
    with as_file(p) as path:
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("ascii")

            # determine the file type from the file extension
            kind = filetype.guess(f)
            if kind is not None:
                mime = kind.mime
            else:
                # For filetypes without magic headers (e.g. SVG), the filetype library
                # doesn't work. In these cases, we try the mimetypes library.
                mime, _ = mimetypes.guess_type(path)

            assert mime is not None, f"Could not determine mime type for {path}"

            return f"data:{mime};base64,{encoded}"


class YamlConfiguration(Configuration):
    def __init__(
        self,
        path_or_handle: Union[str, PathLikeStr, IO[str]],
        base_path: Union[str, PathLikeStr, Traversable, None] = None,
    ) -> None:
        super().__init__()

        if isinstance(path_or_handle, str):
            path_or_handle = Path(path_or_handle)

        if base_path is None:
            assert isinstance(path_or_handle, Path) and os.path.isfile(
                path_or_handle
            ), f"File {path_or_handle} does not exist"
            base_path = os.path.dirname(path_or_handle)

        handle: IO[str]
        if isinstance(path_or_handle, Path):
            handle = path_or_handle.open()
        elif hasattr(path_or_handle, "__fspath__"):
            handle = open(path_or_handle)
        else:
            handle = path_or_handle

        # we want to parse and process special tags (e.g. !image) in yaml files
        # when loading a file with !image, the specified path should be relative to
        # the yaml file itself
        # --> need a custom loader that knows the path to the yaml file
        class CustomLoader(yaml.SafeLoader, CustomLoaderLike):
            def __init__(self, *args: Any, **kwargs: Any) -> None:
                super().__init__(*args, **kwargs)
                assert base_path is not None, "base_path is None"
                self.base_path = base_path

        yaml.add_constructor("!image", image_constructor, CustomLoader)

        self.yaml = yaml.load(handle, Loader=CustomLoader)

    def _get_dict(self) -> dict:
        return self.yaml["module"]
