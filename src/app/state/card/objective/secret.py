from dataclasses import dataclass

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
    