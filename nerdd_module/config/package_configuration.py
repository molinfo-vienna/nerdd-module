import logging

from ..polyfills import files
from .configuration import Configuration
from .dict_configuration import DictConfiguration
from .yaml_configuration import YamlConfiguration

__all__ = ["PackageConfiguration"]

logger = logging.getLogger(__name__)


class PackageConfiguration(Configuration):
    def __init__(self, package: str) -> None:
        super().__init__()

        # get the resource directory
        try:
            root_dir = files(package)
        except ModuleNotFoundError:
            root_dir = None

        self.config: Configuration = DictConfiguration({})
        if root_dir is not None:
            # navigate to the config file
            config_file = root_dir / "nerdd.yml"

            if config_file is not None and config_file.is_file():
                logger.info(f"Found configuration file in package: {config_file}")
                self.config = YamlConfiguration(config_file.open(), base_path=root_dir)
            else:
                self.config = DictConfiguration({})

    def _get_dict(self) -> dict:
        return self.config._get_dict()
