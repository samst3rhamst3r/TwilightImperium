from dataclasses import dataclass
from typing import Final

from app.config.system import WormholeType

from .base import BaseStateObj
from .shared import PlayerOwnable

@dataclass(slots=True, kw_only=True)
class NaaluSpecialTokenState(BaseStateObj, PlayerOwnable):
    pass

@dataclass(slots=True, kw_only=True)
class SpeakerTokenState(BaseStateObj, PlayerOwnable):

    def assign_speaker(self, player_id: str) -> None:
        self.assign_owner(player_id)

    def reassign_speaker(self, player_id: str) -> str:
        return self.reassign_owner(player_id)

    def release_speaker(self) -> str:
        return self.release_owner()

    def is_player_speaker(self, player_id: str) -> bool:
        return self.is_owned_by_player(player_id)

    @property
    def speaker_player_id(self) -> str | None:
        return self.owned_by_player_id

@dataclass(slots=True, kw_only=True)
class NekroAssimilatorTokenState(BaseStateObj):
    assimilated_faction_tech_id: str | None = None

    def assimilate_faction_tech_id(self, faction_tech_id: str) -> None:
        self.assimilated_faction_tech_id = faction_tech_id

    def reset(self) -> None:
        self.assimilated_faction_tech_id = None

    @property
    def is_active(self) -> bool:
        return self.assimilated_faction_tech_id is not None

class InvalidWormholeType(ValueError):
    pass

@dataclass(slots=True, kw_only=True)
class CreussWormholeTokenState(BaseStateObj):
    wormhole_type: Final[WormholeType]
    active_system_id: str | None = None

    def __post_init__(self):
        if self.wormhole_type not in [WormholeType.ALPHA, WormholeType.BETA]:
            raise InvalidWormholeType(f"Invalid wormhole type {self.wormhole_type} for Creuss token. Valid types are: ALPHA, BETA")