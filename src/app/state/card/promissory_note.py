from dataclasses import dataclass
from typing import Final

from app.config.player_color import PlayerColor

from app.state.base.mixins import UUIDandConfigIDStateObj

@dataclass(slots=True, kw_only=True)
class PromissoryNoteCardState(UUIDandConfigIDStateObj):
    issuing_player_color: Final[PlayerColor | None] = None

    @property
    def is_issued_to_player(self) -> bool:
        return self.issuing_player_color is not None

    def is_issued_to(self, player_color: PlayerColor) -> bool:
        return self.issuing_player_color == player_color

    def to_save_dict(self):
        return super().to_save_dict() | {
            "issuing_player_color": self.issuing_player_color
        }

    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        self.issuing_player_color = PlayerColor(data["issuing_player_color"])
