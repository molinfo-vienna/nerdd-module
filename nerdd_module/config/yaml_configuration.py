import base64
import os
import pathlib

import filetype
import yaml

from .configuration import Configuration

__all__ = ["YamlConfiguration"]


def image_constructor(loader, node):
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
    def __init__(self, handle, base_path=None):
        super().__init__()

        if base_path is None:
            assert isinstance(handle, str) and os.path.isfile(handle)
            base_path = os.path.dirname(handle)

        if isinstance(handle, str):
            handle = pathlib.Path(handle)

        if isinstance(base_path, str):
            base_path = pathlib.Path(base_path)

        # we want to parse and process special tags (e.g. !image) in yaml files
        # when loading a file with !image, the specified path should be relative to
        # the yaml file itself
        # --> need a custom loader with the path to the yaml file
        class CustomLoader(yaml.SafeLoader):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.base_path = base_path

        yaml.add_constructor("!image", image_constructor, CustomLoader)

        self.yaml = yaml.load(open(handle, "r"), Loader=CustomLoader)

    def _get_dict(self):
        return self.yaml["module"]
