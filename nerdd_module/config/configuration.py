from abc import ABC, abstractmethod
from typing import Optional

from .models import Module

__all__ = ["Configuration"]


class Configuration(ABC):
    def __init__(self) -> None:
        self._cached_config: Optional[Module] = None

    def get_dict(self) -> Module:
        if self._cached_config is None:
            config = self._get_dict()

            # validate the config
            module = Module(**config)

            self._cached_config = module

        return self._cached_config

    @abstractmethod
    def _get_dict(self) -> dict:
        pass

    def is_empty(self) -> bool:
        return self.get_dict() == {}

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._get_dict()})"
