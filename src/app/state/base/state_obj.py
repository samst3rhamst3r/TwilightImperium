from dataclasses import dataclass, field
from typing import Any, Final, Self
from uuid import uuid4

from app.config.base import NamedConfigObj, IDConfigObj
from app.config.text import BaseTextConfigObj

@dataclass(slots=True, kw_only=True)
class BaseStateObj:
    """Base class for all state objects."""

    def to_save_dict(self) -> dict[str, Any]:
        """Convert the state object to a dictionary for saving."""
        return {}

    @classmethod
    def from_save_dict(cls, **_) -> Self:
        """Create a new instance from a save dictionary."""

    @staticmethod
    def init_from_save_dict(data: dict) -> None:
        """Used to initialize super class fields from a save dictionary. 
        Returns the same dictionary if not edit required.
        Recommended to implement this method in subclasses if initializing super class fields is required.
        """
        return data
    
@dataclass(slots=True, kw_only=True)
class InstancedStateObj(BaseStateObj):
    instance_id: Final[str] = field(default_factory=lambda: uuid4().hex)
    name: Final[str | None] = None

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
        super().__post_init__()
        self.instance_id = self.config.id

@dataclass(slots=True, kw_only=True)
class TextBoundStateObjMixin[TTextConfig: BaseTextConfigObj]:
    """Independent Generic Mixin for text configuration."""
    text_config: TTextConfig

    def to_save_dict(self):
        return {
            "text_config": self.text_config.id
        }
