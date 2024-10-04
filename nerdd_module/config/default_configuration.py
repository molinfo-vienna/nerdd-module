from typing import Any

from stringcase import snakecase  # type: ignore

from ..polyfills import version
from .dict_configuration import DictConfiguration

__all__ = ["DefaultConfiguration"]


class DefaultConfiguration(DictConfiguration):
    def __init__(self, nerdd_module: Any) -> None:
        # generate a name from the module name
        class_name = nerdd_module.__class__.__name__
        if class_name.endswith("Model"):
            # remove the "Model" suffix
            # e.g. SkinDoctorModel -> SkinDoctor
            class_name = class_name[: -len("Model")]

        # convert the class name to snake case
        # e.g. SkinDoctor -> skin_doctor
        name = snakecase(class_name)

        # append version to the configuration
        try:
            module = nerdd_module.__module__
            root_module = module.split(".", 1)[0]
            package_version = version(root_module)
        except ModuleNotFoundError:
            package_version = "0.0.1"

        config = dict(
            name=name,
            version=package_version,
            job_parameters=[],
            result_properties=[],
        )

        super().__init__(config)
