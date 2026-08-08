from dataclasses import dataclass, field
from uuid import uuid4

from .state_obj import StateObj

@dataclass(kw_only=True)
class UUIDInstancedMixin(StateObj):
    instance_id: str = field(init=False, default_factory=lambda: uuid4().hex)

    def to_save_dict(self):
        return super().to_save_dict() | {
            "instance_id": self.instance_id,
        }

    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        self.instance_id = data["instance_id"]

@dataclass(kw_only=True)
class ConfigIDMixin(StateObj):
    config_id: str

    def to_save_dict(self):
        return super().to_save_dict() | {
            "config_id": self.config_id,
        }

    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        self.config_id = data["config_id"]

@dataclass(kw_only=True)
class UUIDandConfigIDMixin(UUIDInstancedMixin, ConfigIDMixin):
    pass

@dataclass(kw_only=True)
class ConfigIDInstanceMixin(UUIDandConfigIDMixin):

    def __post_init__(self):
        super().__post_init__()
        if self.config_id is None:
            raise ValueError("This ConfigIDInstanceMixin must have a config_id supplied.")
        self.instance_id = self.config_id
