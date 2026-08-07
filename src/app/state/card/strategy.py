from dataclasses import dataclass

from app.state.base.protocols import Loadable
from app.state.base.state_obj import ConfigIDBasedStateObj

@dataclass(slots=True, kw_only=True)
class StrategyCardState(ConfigIDBasedStateObj, Loadable):
    pass
