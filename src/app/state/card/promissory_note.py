from dataclasses import dataclass
from typing import Final

from app.state.base.mixins import UUIDInstancedStateObj

@dataclass(kw_only=True)
class PromissoryNoteCardState(UUIDInstancedStateObj):
    issuing_player_id: Final[str]
    holding_player_id: str

    def transfer_to(self, player_id: str) -> None:
        self.holding_player_id = player_id

    def return_to_issuer(self) -> None:
        self.holding_player_id = self.issuing_player_id

    def save(self):
        return super().save() | {
            "issuing_player_id": self.issuing_player_id,
            "holding_player_id": self.holding_player_id
        }

    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        self.issuing_player_id = data["issuing_player_id"]
        self.holding_player_id = data["holding_player_id"]
