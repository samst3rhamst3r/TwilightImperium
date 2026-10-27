from dataclasses import dataclass
from abc import abstractmethod

from .base import Serializable

@dataclass(kw_only=True)
class IDedStateObj(Serializable):
    """A state object that has a class-specific unique identifier."""

    @property
    @abstractmethod
    def id(self) -> str: ...
