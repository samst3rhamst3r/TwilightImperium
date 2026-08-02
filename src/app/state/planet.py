from dataclasses import dataclass

from app.config.planet import PlanetConfig
from app.config.text import PlanetTextConfig

from .base import ConfigIDStateObj
from .shared import Exhaustable, PlayerOwnable

class PlanetAlreadyControlledError(Exception): pass
class PlanetNotControlledError(Exception): pass

@dataclass(slots=True, kw_only=True)
class PlanetState(ConfigIDStateObj[PlanetConfig, PlanetTextConfig], Exhaustable, PlayerOwnable):

    def assign_control(self, player_id: str) -> None:
        self.assign_owner(player_id)

    def reassign_control(self, player_id: str) -> str:
        return self.reassign_owner(player_id)

    def release_control(self) -> str:
        return self.release_owner()

    @property
    def is_controlled(self) -> bool:
        return self.is_owned

    def is_controlled_by_player(self, player_id: str) -> bool:
        return self.is_owned_by_player(player_id)
    