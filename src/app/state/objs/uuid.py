from dataclasses import dataclass, field
from uuid import uuid4

from .config_id import ConfigIDStateObj

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
