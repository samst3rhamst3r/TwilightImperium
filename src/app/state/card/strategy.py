from dataclasses import dataclass

from app.state.base.exhaustible import Exhaustible
from app.state.base.mixins import ConfigIDStateObj
from app.state.base.ownable import PlayerOwnableWithConvenienceProtocol

@dataclass(kw_only=True)
class StrategyCardState(ConfigIDStateObj, Exhaustible, PlayerOwnableWithConvenienceProtocol):
    pass
