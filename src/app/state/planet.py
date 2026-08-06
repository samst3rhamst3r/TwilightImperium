from dataclasses import dataclass
from typing import Self

from app.config.objs.planet import PlanetConfig
from app.config.text_objs import PlanetTextConfig

from .base.state_obj import ConfigIDBasedStateObj, TextBoundStateObjMixin
from .base import Exhaustable, PlayerOwnable

class PlanetAlreadyControlledError(Exception): pass
class PlanetNotControlledError(Exception): pass

@dataclass(slots=True, kw_only=True)
class PlanetState(ConfigIDBasedStateObj[PlanetConfig], TextBoundStateObjMixin[PlanetTextConfig], Exhaustable, PlayerOwnable):

    def to_save_dict(self) -> dict:
        d = ConfigIDBasedStateObj.to_save_dict(self)
        d |= TextBoundStateObjMixin.to_save_dict(self)
        d |= Exhaustable.to_save_dict(self)
        d |= PlayerOwnable.to_save_dict(self)
        return d

    @classmethod
    def from_save_dict(cls, config: PlanetConfig, text_config: PlanetTextConfig, **kwargs) -> Self:
        return cls(config=config, text_config=text_config, **kwargs)
    
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
    