from dataclasses import dataclass

from app.config.strategy import StrategyConfig
from app.config.text import StrategyTextConfig

from .base import ConfigIDStateObj
from .shared import Exhaustable, PlayerOwnable

@dataclass(slots=True, kw_only=True)
class StrategyCardState(ConfigIDStateObj[StrategyConfig, StrategyTextConfig], Exhaustable, PlayerOwnable):
    pass