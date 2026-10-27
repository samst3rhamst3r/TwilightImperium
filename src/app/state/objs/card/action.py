from dataclasses import dataclass
from typing import Final

from app.state.objs import UUIDInstancedStateObj

@dataclass(kw_only=True)
class ActionCardState(UUIDInstancedStateObj):
    flavor_text_index: Final[int]

    def save(self) -> dict:
        return super().save() | {
            "flavor_text_index": self.flavor_text_index
        }

    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        self.flavor_text_index = data["flavor_text_index"]
