from dataclasses import dataclass, field
from typing import Final, Any, Self
from collections.abc import Mapping
from uuid import uuid4

from app.config.base import NamedConfigObj, IDConfigObj
from app.config.text import BaseTextConfigObj

@dataclass(slots=True, kw_only=True)
class BaseStateObj:
    """Base class for all state objects."""

    @classmethod
    def restore(cls, data: Mapping[str, Any]) -> Self:
        """Restore the state from the given data."""
        return cls(**data)

@dataclass(slots=True, kw_only=True)
class InstancedStateObj(BaseStateObj):
    instance_id: Final[str] = field(default_factory=lambda: uuid4().hex)
    name: Final[str | None] = None

@dataclass(slots=True, kw_only=True)
class ConfigBasedStateObj[TConfig: NamedConfigObj, TTextConfig: BaseTextConfigObj](InstancedStateObj):
    config: TConfig
    text_config: TTextConfig

    def __post_init__(self):
        self.name = self.config.name

@dataclass(slots=True, kw_only=True)
class ConfigIDBasedStateObj[TConfig: IDConfigObj, TTextConfig: BaseTextConfigObj](ConfigBasedStateObj[TConfig, TTextConfig]):

    def __post_init__(self):
        self.instance_id = self.config.id
        super().__post_init__()
