from dataclasses import dataclass

from app.state.base.mixins import UUIDandConfigIDStateObj

@dataclass(slots=True, kw_only=True)
class ActionCardState(UUIDandConfigIDStateObj):
    flavor_text_index: int

    def to_save_dict(self) -> dict:
        return super().to_save_dict(self) | {
            "flavor_text_index": self.flavor_text_index
        }

    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        self.flavor_text_index = data["flavor_text_index"]
