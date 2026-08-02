from dataclasses import dataclass, field
from typing import Final
from uuid import uuid4
from abc import ABC, abstractmethod

from app.config.base import NamedConfigObj, IDConfigObj
from app.config.text import BaseTextConfigObj

@dataclass(slots=True, kw_only=True)
class BaseStateObj(ABC):
    """Base class for all state objects."""
    _instance_id: Final[str] = field(init=False, default_factory=lambda: uuid4().hex)

    @property
    def instance_id(self):
        return self._instance_id

    @property
    @abstractmethod
    def name(self) -> str:
        pass

@dataclass(slots=True, kw_only=True)
class ConfigBasedStateObj[TConfig: NamedConfigObj, TTextConfig: BaseTextConfigObj](BaseStateObj):
    config: TConfig
    text_config: TTextConfig

    @property
    def name(self) -> str:
        return self.config.name

@dataclass(slots=True, kw_only=True)
class ConfigIDBasedStateObj[TConfig: IDConfigObj, TTextConfig: BaseTextConfigObj](ConfigBasedStateObj[TConfig, TTextConfig]):

    def __post_init__(self):
        self.instance_id = self.config.id
