from dataclasses import dataclass
from typing import Final

from app.config.player_color import PlayerColor

from app.state.base.mixins import UUIDInstancedStateObj

@dataclass(kw_only=True)
class PromissoryNoteCardState(UUIDInstancedStateObj):
    issuing_player_color: Final[PlayerColor | None] = None

    @property
    def is_issued_to_player(self) -> bool:
        return self.issuing_player_color is not None

    def is_issued_to(self, player_color: PlayerColor) -> bool:
        return self.issuing_player_color == player_color

    def save(self):
        return super().save() | {
            "issuing_player_color": self.issuing_player_color
        }

    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        issuing_player_color = data["issuing_player_color"]
        self.issuing_player_color = PlayerColor(issuing_player_color) if issuing_player_color is not None else None
