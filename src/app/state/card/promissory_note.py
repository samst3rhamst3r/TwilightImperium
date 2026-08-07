from dataclasses import dataclass
from typing import Final, Self

from app.config.player_color import PlayerColor

from app.state.base import ConfigBoundStateObj, PlayerOwnable

@dataclass(slots=True, kw_only=True)
class PromissoryNoteCardState(ConfigBoundStateObj, PlayerOwnable):
    issuing_player_color: Final[PlayerColor | None] = None

    @property
    def is_issued_to_player(self) -> bool:
        return self.issuing_player_color is not None

    def is_issued_to(self, player_color: PlayerColor) -> bool:
        return self.issuing_player_color == player_color

    def to_save_dict(self):
        d  = ConfigBoundStateObj.to_save_dict(self)
        d |= PlayerOwnable.to_save_dict(self)
        return d | {
            "issuing_player_color": self.issuing_player_color
        }

    @classmethod
    def from_save_dict(cls, issuing_player_color: str | None, **kwargs) -> Self:
        if issuing_player_color is not None:
            issuing_player_color = PlayerColor(issuing_player_color)
        return cls(issuing_player_color=issuing_player_color, **kwargs)
    