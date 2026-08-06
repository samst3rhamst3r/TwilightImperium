from dataclasses import dataclass
from typing import Self

from app.config.objs.strategy_card import StrategyCardConfig
from app.config.text_objs import StrategyCardTextConfig

from app.state.base.state_obj import ConfigIDBasedStateObj, TextBoundStateObjMixin
from app.state.base import Exhaustable, PlayerOwnable

@dataclass(slots=True, kw_only=True)
class StrategyCardState(ConfigIDBasedStateObj[StrategyCardConfig], TextBoundStateObjMixin[StrategyCardTextConfig], Exhaustable, PlayerOwnable):

    @classmethod
    def from_save_dict(cls, config: StrategyCardConfig, text_config: StrategyCardTextConfig, **kwargs) -> Self:
        return cls(config=config, text_config=text_config, **kwargs)

    def to_save_dict(self):
        d = ConfigIDBasedStateObj[StrategyCardConfig].to_save_dict(self)
        d |= TextBoundStateObjMixin[StrategyCardTextConfig].to_save_dict(self)
        d |= Exhaustable.to_save_dict(self)
        d |= PlayerOwnable.to_save_dict(self)
        return d

