import logging
import os
from typing import Optional

from .configuration import Configuration
from .dict_configuration import DictConfiguration
from .yaml_configuration import YamlConfiguration

__all__ = ["SearchYamlConfiguration"]

logger = logging.getLogger(__name__)


class SearchYamlConfiguration(DictConfiguration):
    def __init__(self, start: str, base_path: Optional[str] = None) -> None:
        # provide a default configuration if no configuration file is found
        config: Configuration = DictConfiguration({})

        if start is not None:
            # start at the directory containing the file where nerdd_module_class is
            # defined and go up the directory tree until nerdd.yml is found (or root is
            # reached)
            leaf = start
            while True:
                if os.path.isfile(os.path.join(leaf, "nerdd.yml")):
                    default_config_file = os.path.join(leaf, "nerdd.yml")
                    break
                elif leaf == os.path.dirname(leaf):  # reached root
                    default_config_file = None
                    break
                leaf = os.path.dirname(leaf)

            if default_config_file is not None:
                logger.info(f"Found configuration file in project directory: {default_config_file}")
                config = YamlConfiguration(default_config_file, base_path)

        super().__init__(config._get_dict())
