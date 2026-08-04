from dataclasses import dataclass

from app.config.strategy import StrategyConfig
from app.config.text import StrategyTextConfig

from app.state.base.state_obj import ConfigIDBasedStateObj, TextBoundStateObjMixin
from app.state.base import Exhaustable, PlayerOwnable

@dataclass(slots=True, kw_only=True)
class StrategyCardState(ConfigIDBasedStateObj[StrategyConfig], TextBoundStateObjMixin[StrategyTextConfig], Exhaustable, PlayerOwnable):
    pass