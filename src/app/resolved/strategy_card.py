from dataclasses import dataclass

from app.config.objs.strategy_card import StrategyCardConfig
from app.state.card import StrategyCardState

from .base import BaseResolvedObj
from .exhaust import IsExhaustibleProtocol

@dataclass(slots=True, frozen=True)
class ResolvedStrategyCard(BaseResolvedObj[StrategyCardState, StrategyCardConfig], IsExhaustibleProtocol):
    pass