from dataclasses import dataclass

from app.config.strategy import StrategyConfig
from app.config.text import StrategyTextConfig

from ..base import ConfigIDBasedStateObj
from ..shared import Exhaustable, PlayerOwnable

@dataclass(slots=True, kw_only=True)
class StrategyCardState(ConfigIDBasedStateObj[StrategyConfig, StrategyTextConfig], Exhaustable, PlayerOwnable):
    pass