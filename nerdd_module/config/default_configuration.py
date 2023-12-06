from .configuration import Configuration

__all__ = ["DefaultConfiguration"]


class DefaultConfiguration(Configuration):
    def __init__(self, nerdd_module):
        super().__init__()

        # we do not use default values at the moment
        # feel free to add values here if needed
        self.config = {}

    def _get_dict(self):
        return self.config
