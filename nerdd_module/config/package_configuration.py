try:
    # works in python 3.9+
    from importlib.resources import files
except ImportError:
    from importlib_resources import files

from .configuration import Configuration
from .dict_configuration import DictConfiguration
from .yaml_configuration import YamlConfiguration

__all__ = ["PackageConfiguration"]


class PackageConfiguration(Configuration):
    def __init__(self, package):
        super().__init__()

        # get the resource directory
        root_dir = files(package)

        # navigate to the config file
        config_file = root_dir / "nerdd.yml"

        if config_file is not None and config_file.exists():
            self.config = YamlConfiguration(config_file, base_path=root_dir)
        else:
            self.config = DictConfiguration({})

    def _get_dict(self):
        return self.config.get_dict()
