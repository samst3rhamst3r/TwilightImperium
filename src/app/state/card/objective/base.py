from dataclasses import dataclass

from app.state.base.mixins import ConfigIDInstancedStateObj

@dataclass(slots=True, kw_only=True)
class ObjectiveCardState(ConfigIDInstancedStateObj):
    pass