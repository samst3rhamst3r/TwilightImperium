from dataclasses import dataclass

from app.state.base.exhaustible import Exhaustible
from app.state.base.mixins import ConfigIDStateObj

@dataclass(kw_only=True)
class StrategyCardState(ConfigIDStateObj, Exhaustible):
    exhausted: bool = False
