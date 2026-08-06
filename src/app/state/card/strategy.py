from dataclasses import dataclass

from app.config.objs.strategy_card import StrategyCardConfig

from app.state.base.state_obj import ConfigIDBasedStateObj
from app.state.base import Exhaustable, PlayerOwnable

@dataclass(slots=True, kw_only=True)
class StrategyCardState(ConfigIDBasedStateObj, Exhaustable, PlayerOwnable):

    def to_save_dict(self):
        d = ConfigIDBasedStateObj[StrategyCardConfig].to_save_dict(self)
        d |= Exhaustable.to_save_dict(self)
        d |= PlayerOwnable.to_save_dict(self)
        return d
