from dataclasses import dataclass
from typing import Self

from app.state.base import PlayerOwnable

from .base import ObjectiveCardState

@dataclass(slots=True, kw_only=True)
class SecretObjectiveCardState(ObjectiveCardState, PlayerOwnable):
    scored: bool = False

    def to_save_dict(self):
        d = ObjectiveCardState.to_save_dict(self)
        d |= PlayerOwnable.to_save_dict(self)
        return d | {
            "scored": self.scored
        }
    
    @classmethod
    def from_save_dict(cls, data: dict) -> Self:
        return cls(
            scored=data["scored"],
            **ObjectiveCardState.init_from_save_dict(data),
            **PlayerOwnable.init_from_save_dict(data)
        )
    