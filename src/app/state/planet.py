from dataclasses import dataclass

from .base.ownable import PlayerOwnableMixin
from .base.mixins import ConfigIDInstancedStateObj

class PlanetAlreadyControlledError(Exception): 
    pass
class PlanetNotControlledError(Exception): 
    pass

@dataclass(slots=True, kw_only=True)
class PlanetState(ConfigIDInstancedStateObj, PlayerOwnableMixin):

    def assign_control(self, player_id: str) -> None:
        self.ownable.assign_owner(player_id)

    def reassign_control(self, player_id: str) -> str:
        return self.ownable.reassign_owner(player_id)

    def release_control(self) -> str:
        return self.ownable.release_owner()

    @property
    def is_controlled(self) -> bool:
        return self.ownable.is_owned

    def is_controlled_by_player(self, player_id: str) -> bool:
        return self.ownable.is_owned_by_player(player_id)
    