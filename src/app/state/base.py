from dataclasses import dataclass, field
from typing import Final
from uuid import uuid4

from app.config.base import NamedConfigObj, IDConfigObj
from app.config.text import BaseTextConfigObj

@dataclass(slots=True, kw_only=True)
class BaseStateObj:
    """Base class for all state objects."""

@dataclass(slots=True, kw_only=True)
class InstancedStateObj(BaseStateObj):
    instance_id: Final[str] = field(default_factory=lambda: uuid4().hex)
    name: Final[str | None] = None

@dataclass(slots=True, kw_only=True)
class ConfigBoundStateObj[TConfig: NamedConfigObj](InstancedStateObj):
    config: TConfig

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
