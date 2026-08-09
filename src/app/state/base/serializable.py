from dataclasses import dataclass
from typing import Self
from abc import ABC, abstractmethod

@dataclass(init=False, kw_only=True)
class Serializable(ABC):
    """Top-level class used for type-checkers and to provide a common interface for all state objects.
    All objects at this level are serializable via "save", "load", and "init_from_save" methods
    """

    @abstractmethod
    def save(self) -> dict: ...

    @abstractmethod
    def init_from_save(self, data: dict) -> None: ...

    @classmethod
    def load(cls, data: dict) -> Self:
        obj = cls.__new__(cls)
        obj.init_from_save(data)
        return obj
