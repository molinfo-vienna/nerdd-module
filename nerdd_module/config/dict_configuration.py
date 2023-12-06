from .configuration import Configuration

__all__ = ["DictConfiguration"]


class DictConfiguration(Configuration):
    def __init__(self, config):
        super().__init__()

        self.config = config

    def _get_dict(self):
        return self.config
