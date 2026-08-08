from dataclasses import dataclass

from app.config.objs.planet import PlanetConfig
from app.state.planet import PlanetState 

from .base import BaseResolvedObj

# Does not need PlayerOwnableMixin because it will forward to State object which resolves that forwarding already
from .shared.protocols import ExhaustibleMixin

@dataclass(slots=True, kw_only=True)
class ResolvedPlanet(BaseResolvedObj[PlanetState, PlanetConfig], ExhaustibleMixin):

    def assign_control(self, player_id: str) -> None:
        self.state.assign_control(player_id)

    def reassign_control(self, player_id: str) -> str:
        return self.state.reassign_control(player_id)

    def release_control(self) -> str:
        return self.state.release_control()

    @property
    def is_controlled(self) -> bool:
        return self.state.is_controlled

    def is_controlled_by_player(self, player_id: str) -> bool:
        return self.state.is_controlled_by_player(player_id)
    