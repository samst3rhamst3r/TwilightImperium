from dataclasses import dataclass

from app.state.base.state_obj import ConfigIDInstanceMixin

@dataclass(slots=True, kw_only=True)
class ObjectiveCardState(ConfigIDInstanceMixin):
    pass