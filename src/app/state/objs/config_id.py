from dataclasses import dataclass

from app.state import IDedStateObj

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

