from dataclasses import dataclass, field

from app.state.base.exhaustable import Exhaustable
from app.state.base.protocols import Loadable
from app.state.base.state_obj import ConfigIDBasedStateObj

@dataclass(slots=True, kw_only=True)
class StrategyCardState(ConfigIDBasedStateObj, Loadable):
    exhaustable_obj: Exhaustable = field(default_factory=Exhaustable)
