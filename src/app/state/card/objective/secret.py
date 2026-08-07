from dataclasses import dataclass

from app.state.base.protocols import Loadable

from .base import ObjectiveCardState

@dataclass(slots=True, kw_only=True)
class SecretObjectiveCardState(ObjectiveCardState, Loadable):
    scored: bool = False

    def to_save_dict(self):
        d = super().to_save_dict()
        return d | {
            "scored": self.scored
        }
    