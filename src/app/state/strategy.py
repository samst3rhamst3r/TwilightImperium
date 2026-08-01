from dataclasses import dataclass

from app.config.strategy import StrategyConfig
from app.config.text import StrategyTextConfig

from .base import BaseStateObj
from .shared import Exhaustable

@dataclass(slots=True, kw_only=True)
class StrategyCardState(BaseStateObj[StrategyConfig, StrategyTextConfig], Exhaustable):
    pass