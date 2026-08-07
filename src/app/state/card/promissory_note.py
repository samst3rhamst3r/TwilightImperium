from dataclasses import dataclass
from typing import Final

from app.config.player_color import PlayerColor

from app.state.base import InstancedStateObj
from app.state.base.protocols import Loadable

@dataclass(slots=True, kw_only=True)
class PromissoryNoteCardState(InstancedStateObj, Loadable):
    issuing_player_color: Final[PlayerColor | None] = None

    @property
    def is_issued_to_player(self) -> bool:
        return self.issuing_player_color is not None

    def is_issued_to(self, player_color: PlayerColor) -> bool:
        return self.issuing_player_color == player_color

    def to_save_dict(self):
        d  = super().to_save_dict()
        return d | {
            "issuing_player_color": self.issuing_player_color
        }

    @staticmethod
    def init_from_save_dict(data: dict):
        issuing_player_color = data.get("issuing_player_color")
        if issuing_player_color is not None:
            data["issuing_player_color"] = PlayerColor(issuing_player_color)
        return data

    @classmethod
    def from_save_dict(cls, issuing_player_color: str | None, **kwargs):
        kwargs = cls.init_from_save_dict(kwargs)
        return cls(**kwargs)
