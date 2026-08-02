from dataclasses import dataclass, field
from typing import Self
from uuid import uuid4

from app.config.base import BaseConfigObj, IDConfigObj
from app.config.text import BaseTextConfigObj

@dataclass(slots=True, kw_only=True)
class BaseStateObj[TConfig: BaseConfigObj, TTextConfig: BaseTextConfigObj]:
    """Base class for all state objects."""
    config: TConfig
    text_config: TTextConfig

@dataclass(slots=True, kw_only=True)
class UUIDStateObj[TConfig: BaseConfigObj, TTextConfig: BaseTextConfigObj](BaseStateObj[TConfig, TTextConfig]):
    _instance_id: str = field(init=False, default_factory=lambda: uuid4().hex)

    @property
    def instance_id(self) -> str:
        return self._instance_id
    
    @classmethod
    def restore(cls, config: TConfig, text_config: TTextConfig, instance_id: str, **kwargs) -> Self:
        obj = cls(config=config, text_config=text_config, **kwargs)
        obj._instance_id = instance_id
        return obj

@dataclass(slots=True, kw_only=True)
class ConfigIDStateObj[TConfig: IDConfigObj, TTextConfig: BaseTextConfigObj](BaseStateObj[TConfig, TTextConfig]):

    def __post_init__(self):
        self._instance_id = self.config.id