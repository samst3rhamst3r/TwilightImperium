from dataclasses import dataclass, field
from uuid import uuid4
from abc import abstractmethod

from app.state.base.serializable import Serializable

@dataclass(kw_only=True)
class IDedStateObj(Serializable):
    """A state object that has a class-specific unique identifier."""

    @property
    @abstractmethod
    def id(self) -> str: ...

@dataclass(kw_only=True)
class ConfigIDStateObj(IDedStateObj):
    config_id: str

    @property
    def id(self) -> str:
        return self.config_id
    
    def save(self):
        return super().save() | {
            "config_id": self.config_id,
        }

    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        self.config_id = data["config_id"]

@dataclass(kw_only=True)
class UUIDInstancedStateObj(ConfigIDStateObj):
    instance_id: str = field(init=False, default_factory=lambda: uuid4().hex)

    @property
    def id(self) -> str:
        return self.instance_id
    
    def save(self):
        return super().save() | {
            "instance_id": self.instance_id,
        }

    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        self.instance_id = data["instance_id"]
