import base64
import os
from os import PathLike
from pathlib import Path
from typing import Any, Optional, Union

import filetype  # type: ignore
import yaml
from typing_extensions import Protocol

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
        handle: Union[str, PathLike[str]],
        base_path: Union[str, PathLike[str], None] = None,
    ) -> None:
        super().__init__()

        if isinstance(handle, str):
            handle = Path(handle)

        if base_path is None:
            assert os.path.isfile(handle), f"File {handle} does not exist"
            base_path = os.path.dirname(handle)
        else:
            base_path = Path(base_path)

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

        self.yaml = yaml.load(open(handle, "r"), Loader=CustomLoader)

    def _get_dict(self) -> dict:
        return self.yaml["module"]
