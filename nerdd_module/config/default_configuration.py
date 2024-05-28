from stringcase import snakecase

from ..polyfills import version
from .configuration import Configuration

__all__ = ["DefaultConfiguration"]


class DefaultConfiguration(Configuration):
    def __init__(self, nerdd_module):
        super().__init__()

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
            version_ = version(root_module)
        except ModuleNotFoundError:
            pass

        self.config = dict(
            name=name,
            version=version_,
            task="molecular_property_prediction",
            job_parameters=[],
            result_properties=[],
        )

    def _get_dict(self):
        return self.config
