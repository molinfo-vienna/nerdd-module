from .configuration import Configuration

__all__ = ["DictConfiguration"]


class DictConfiguration(Configuration):
    def __init__(self, config: dict) -> None:
        super().__init__()
        self._config = config

    def _get_dict(self) -> dict:
        return self._config
