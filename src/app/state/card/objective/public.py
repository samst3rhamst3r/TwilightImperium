from dataclasses import dataclass

from .base import ObjectiveCardState

@dataclass(slots=True, kw_only=True)
class PublicObjectiveCardState(ObjectiveCardState):
    pass