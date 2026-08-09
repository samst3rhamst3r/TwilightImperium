from dataclasses import dataclass

from app.state.base.mixins import UUIDInstancedStateObj

@dataclass(slots=True, kw_only=True)
class ActionCardState(UUIDInstancedStateObj):
    flavor_text_index: int

    def save(self) -> dict:
        return super().save() | {
            "flavor_text_index": self.flavor_text_index
        }

    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        self.flavor_text_index = data["flavor_text_index"]
