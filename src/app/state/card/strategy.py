from dataclasses import dataclass
from typing import Self

from app.config.strategy import StrategyConfig
from app.config.text import StrategyTextConfig

from app.state.base.state_obj import ConfigIDBasedStateObj, TextBoundStateObjMixin
from app.state.base import Exhaustable, PlayerOwnable

@dataclass(slots=True, kw_only=True)
class StrategyCardState(ConfigIDBasedStateObj[StrategyConfig], TextBoundStateObjMixin[StrategyTextConfig], Exhaustable, PlayerOwnable):

    def to_save_dict(self):
        d = ConfigIDBasedStateObj.to_save_dict(self)
        d |= TextBoundStateObjMixin.to_save_dict(self)
        d |= Exhaustable.to_save_dict(self)
        d |= PlayerOwnable.to_save_dict(self)
        return d

    @classmethod
    def from_save_dict(cls, config: StrategyConfig, text_config: StrategyTextConfig, **kwargs) -> Self:
        return cls(config=config, text_config=text_config, **kwargs)