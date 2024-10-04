import sys
from typing import Any, Optional

__all__ = ["get_file_path_to_instance"]


def get_file_path_to_instance(instance: Any) -> Optional[str]:
    # get the class of the provided class instance, e.g. <CypstrateModel>
    instance_class = instance.__class__

    # get the module name of the class
    # e.g. "cypstrate.cypstrate_model"
    instance_module_name = instance_class.__module__

    # get the file where the nerdd module class is defined
    # e.g. "/path/to/cypstrate/cypstrate_model.py"
    module = sys.modules[instance_module_name]

    if hasattr(module, "__file__") and module.__file__ is not None:
        path = module.__file__
    else:
        # if the module has no __file__ attribute, return None
        path = None

    return path
