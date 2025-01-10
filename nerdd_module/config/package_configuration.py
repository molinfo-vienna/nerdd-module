import logging

from ..polyfills import files
from .configuration import Configuration
from .dict_configuration import DictConfiguration
from .yaml_configuration import YamlConfiguration

__all__ = ["PackageConfiguration"]

logger = logging.getLogger(__name__)


class PackageConfiguration(Configuration):
    def __init__(self, package: str, filename: str = "nerdd.yml") -> None:
        super().__init__()

        package_path = package.split(".")
        package_root = package_path[0]
        remaining_path = package_path[1:]

        # get the resource directory
        root_dir = files(package_root)
        assert root_dir is not None

        self.config: Configuration = DictConfiguration({})

        # navigate to the config file
        config_file = root_dir.joinpath(*remaining_path, filename)
        assert config_file is not None and config_file.is_file()

        logger.info(f"Found configuration file in package: {config_file}")
        self.config = YamlConfiguration(
            config_file.open(), base_path=root_dir.joinpath(*remaining_path)
        )

    def _get_dict(self) -> dict:
        return self.config._get_dict()
