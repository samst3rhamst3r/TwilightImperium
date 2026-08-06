from dataclasses import dataclass, field
from typing import Final, Self
from uuid import uuid4

from app.config.base import NamedConfigObj, IDConfigObj
from app.config.text import BaseTextConfigObj

@dataclass(slots=True, kw_only=True)
class BaseStateObj:
    """Base class for all state objects."""

    @classmethod
    def new_game(cls, **kwargs) -> Self:
        return cls(**kwargs)

    @classmethod
    def from_save_dict(cls, data: dict) -> Self:
        return cls(**data)
    
    def to_save_dict(self) -> dict:
        raise NotImplementedError("Subclasses must implement this method")

@dataclass(slots=True, kw_only=True)
class InstancedStateObj(BaseStateObj):
    instance_id: Final[str] = field(default_factory=lambda: uuid4().hex)

    def to_save_dict(self):
        return {
            "instance_id": self.instance_id,
            "name": self.name
        }

@dataclass(slots=True, kw_only=True)
class ConfigBoundStateObj(InstancedStateObj):
    config_id: str

    def to_save_dict(self):
        d = super().to_save_dict()
        return d | {
            "config_id": self.config_id
        }

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
