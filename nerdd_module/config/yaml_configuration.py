import base64
import os
from pathlib import Path
from typing import IO, Any, Optional, Union

import filetype  # type: ignore
import yaml
from typing_extensions import Protocol

from ..polyfills import PathLikeStr
from .configuration import Configuration

__all__ = ["YamlConfiguration"]


class CustomLoaderLike(Protocol):
    base_path: Path

    def construct_scalar(self, node: yaml.ScalarNode) -> str: ...


def image_constructor(loader: CustomLoaderLike, node: yaml.Node) -> str:
    assert isinstance(node, yaml.ScalarNode)

    # obtain the actual file path from the scalar string node
    filepath = loader.construct_scalar(node)

    # load the image from the provided logo path and convert it to base64
    with open(loader.base_path / filepath, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")

        # determine the file type from the file extension
        kind = filetype.guess(f)
        assert kind is not None

        return f"data:{kind.mime};base64,{encoded}"


class YamlConfiguration(Configuration):
    def __init__(
        self,
        path_or_handle: Union[str, PathLikeStr, IO[str]],
        base_path: Union[str, PathLikeStr, None] = None,
    ) -> None:
        super().__init__()

        if isinstance(path_or_handle, str):
            path_or_handle = Path(path_or_handle)

        if base_path is None:
            assert isinstance(path_or_handle, Path) and os.path.isfile(
                path_or_handle
            ), f"File {path_or_handle} does not exist"
            base_path = os.path.dirname(path_or_handle)
        else:
            base_path = Path(base_path)

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
                self.base_path = Path(base_path)

        yaml.add_constructor("!image", image_constructor, CustomLoader)

        self.yaml = yaml.load(handle, Loader=CustomLoader)

    def _get_dict(self) -> dict:
        return self.yaml["module"]
