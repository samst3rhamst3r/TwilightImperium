from dataclasses import dataclass

from app.state.shared import PlayerOwnable

from .base import ObjectiveCardState

@dataclass(slots=True, kw_only=True)
class SecretObjectiveState(ObjectiveCardState, PlayerOwnable):
    pass