from dataclasses import dataclass

from app.state.base.state_obj import ConfigIDBasedStateObj

@dataclass(slots=True, kw_only=True)
class ObjectiveCardState(ConfigIDBasedStateObj):
    pass