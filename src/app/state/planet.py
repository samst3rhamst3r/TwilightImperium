from dataclasses import dataclass

from app.state.base.protocols import Loadable

from .base.state_obj import ConfigIDBasedStateObj

class PlanetAlreadyControlledError(Exception): 
    pass
class PlanetNotControlledError(Exception): 
    pass

@dataclass(slots=True, kw_only=True)
class PlanetState(ConfigIDBasedStateObj, Loadable):

    def assign_control(self, player_id: str) -> None:
        self.ownable_obj.assign_owner(player_id)

    def reassign_control(self, player_id: str) -> str:
        return self.ownable_obj.reassign_owner(player_id)

    def release_control(self) -> str:
        return self.ownable_obj.release_owner()

    @property
    def is_controlled(self) -> bool:
        return self.ownable_obj.is_owned

    def is_controlled_by_player(self, player_id: str) -> bool:
        return self.ownable_obj.is_owned_by_player(player_id)
    