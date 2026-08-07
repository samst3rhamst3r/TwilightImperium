from dataclasses import dataclass

from app.state.base.protocols import Loadable

from .base import ObjectiveCardState

@dataclass(slots=True, kw_only=True)
class PublicObjectiveCardState(ObjectiveCardState, Loadable):
    pass