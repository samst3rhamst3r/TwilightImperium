from dataclasses import dataclass, field
from typing import Any, Final, Self, Protocol
from uuid import uuid4
from abc import ABC, abstractmethod

from app.config.base import NamedConfigObj, IDConfigObj
from app.config.text import BaseTextConfigObj

@dataclass(slots=True, kw_only=True)
class BaseStateObj(ABC):
    """Base class for all state objects."""

    @abstractmethod
    def to_save_dict(self) -> dict[str, Any]:
        """Convert the state object to a dictionary for saving."""
        return {}

    @classmethod
    @abstractmethod
    def from_save_dict(cls, **kwargs) -> Self:
        """Create a new instance from a save dictionary."""

@dataclass(slots=True, kw_only=True)
class InstancedStateObj(BaseStateObj):
    instance_id: Final[str] = field(default_factory=lambda: uuid4().hex)
    name: Final[str | None] = None

    @abstractmethod
    def to_save_dict(self):
        d = super().to_save_dict()
        return d | {
            "instance_id": self.instance_id,
            "name": self.name
        }

@dataclass(slots=True, kw_only=True)
class ConfigBoundStateObj[TConfig: NamedConfigObj](InstancedStateObj):
    config: TConfig

    def to_save_dict(self):
        d = super().to_save_dict()
        return d | {
            "config": self.config.id
        }
    
    def __post_init__(self):
        self.name = self.config.name

@dataclass(slots=True, kw_only=True)
class ConfigIDBasedStateObj[TConfig: IDConfigObj](ConfigBoundStateObj[TConfig]):

    def __post_init__(self):
        self.instance_id = self.config.id
        super().__post_init__()

@dataclass(slots=True, kw_only=True)
class TextBoundStateObjMixin[TTextConfig: BaseTextConfigObj]:
    """Independent Generic Mixin for text configuration."""
    text_config: TTextConfig
