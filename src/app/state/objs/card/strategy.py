from dataclasses import dataclass

from app.state.objs import ConfigIDStateObj, Exhaustible, PlayerOwnableWithConvenienceProtocol

@dataclass(kw_only=True)
class StrategyCardState(ConfigIDStateObj, Exhaustible, PlayerOwnableWithConvenienceProtocol):
    pass
