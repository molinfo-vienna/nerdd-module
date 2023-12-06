from .configuration import Configuration

__all__ = ["MergedConfiguration"]


class MergedConfiguration(Configuration):
    def __init__(self, *configs):
        super().__init__()

        self.config = dict()

        for c in configs:
            self.config.update(c._get_dict())

    def _get_dict(self):
        return self.config
