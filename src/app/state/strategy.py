
from .shared import Exhaustable, BaseStateObj
from app.config.strategy import StrategyConfig

class StrategyCardState(BaseStateObj[StrategyConfig], Exhaustable):
    pass