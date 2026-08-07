from dataclasses import dataclass, field
from typing import Final, Self
from uuid import uuid4

from .exhaustable import Exhaustable
from .ownable import PlayerOwnable
from .protocols import Savable, MixinInitializer

@dataclass(slots=True, kw_only=True)
class BaseStateObj(Savable, MixinInitializer):
    exhaustable_obj: Exhaustable | None = None
    ownable_obj: PlayerOwnable | None = None

    @staticmethod
    def init_from_save_dict(data: dict) -> dict:
        if "exhaustable_obj" in data:
            data["exhaustable_obj"] = Exhaustable.init_from_save_dict(data["exhaustable_obj"])
        if "ownable_obj" in data:
            data["ownable_obj"] = PlayerOwnable.init_from_save_dict(data["ownable_obj"])
        return data

    def to_save_dict(self) -> dict:
        d = {}
        if self.exhaustable_obj is not None:
            d["exhaustable_obj"] = self.exhaustable_obj.to_save_dict()
        if self.ownable_obj is not None:
            d["ownable_obj"] = self.ownable_obj.to_save_dict()
        return d

@dataclass(slots=True, kw_only=True)
class InstancedStateObj(BaseStateObj):
    instance_id: Final[str] = field(default_factory=lambda: uuid4().hex)
    config_id: str | None = None

    def to_save_dict(self):
        return super().to_save_dict() | {
            "instance_id": self.instance_id,
            "config_id": self.config_id
        }

@dataclass(slots=True, kw_only=True)
class ConfigIDBasedStateObj(InstancedStateObj):

    def __post_init__(self):
        super().__post_init__()
        if self.config_id is None:
            raise ValueError("This ConfigIDBasedStateObj must have a config_id supplied.")
        self.instance_id = self.config_id
