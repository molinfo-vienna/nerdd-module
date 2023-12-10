import os
import sys

from .configuration import Configuration
from .default_configuration import DefaultConfiguration
from .dict_configuration import DictConfiguration
from .merged_configuration import MergedConfiguration
from .package_configuration import PackageConfiguration
from .yaml_configuration import YamlConfiguration

__all__ = ["AutoConfiguration"]


class AutoConfiguration(Configuration):
    def __init__(self, nerdd_module):
        super().__init__()

        # get the class of the nerdd module, e.g. <CypstrateModel>
        nerdd_module_class = nerdd_module.__class__

        # get the module name of the nerdd module class
        # e.g. "cypstrate.cypstrate_model"
        python_module = nerdd_module_class.__module__

        # get the root module name, e.g. "cypstrate"
        root_module = python_module.split(".")[0]

        # collect configurations that are used
        configs = []

        # 1. module has a default configuration (containing default values)
        configs.append(DefaultConfiguration(nerdd_module))

        # 2. module can be configured via a yaml file
        # 2.a search for nerdd.yml in the file tree
        # start at the directory containing the file where nerdd_module_class is
        # defined and go up the directory tree until nerdd.yml is found
        leaf = sys.modules[nerdd_module_class.__module__].__file__ or ""
        while True:
            if os.path.isfile(os.path.join(leaf, "nerdd.yml")):
                default_config_file = os.path.join(leaf, "nerdd.yml")
                break
            elif leaf == os.path.dirname(leaf):
                default_config_file = None
                break
            leaf = os.path.dirname(leaf)

        if default_config_file is not None:
            configs.append(YamlConfiguration(default_config_file))

        # 2.b search for nerdd.yml in the package (submodule package_name.data)
        data_module = f"{root_module}.data"
        configs.append(PackageConfiguration(data_module))

        # 3. module can be configured via the method _get_config in the module
        if hasattr(nerdd_module, "_get_config"):
            configs.append(DictConfiguration(nerdd_module._get_config()))

        self.delegate = MergedConfiguration(*configs)

    def _get_dict(self):
        return self.delegate._get_dict()
