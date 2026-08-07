from dataclasses import dataclass

from app.state.player import PlayerState
from app.config.objs.faction import FactionConfig

from .base import BaseResolvedObj

@dataclass(slots=True, frozen=True)
class ResolvedPlayer(BaseResolvedObj[PlayerState, FactionConfig]):

    def replenish_commodities(self) -> None:
        self.state.set_commodities(self.config.max_commodities)
