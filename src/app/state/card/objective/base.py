from dataclasses import dataclass

from app.state.base.mixins import ConfigIDInstanceMixin

@dataclass(slots=True, kw_only=True)
class ObjectiveCardState(ConfigIDInstanceMixin):
    pass