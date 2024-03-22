from .configuration import Configuration

__all__ = ["DefaultConfiguration"]


class DefaultConfiguration(Configuration):
    def __init__(self, nerdd_module):
        super().__init__()

        self.config = dict(
            task="molecular_property_prediction",
            job_parameters=[],
            result_properties=[],
        )

    def _get_dict(self):
        return self.config
