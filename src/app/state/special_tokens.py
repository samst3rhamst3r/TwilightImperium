from dataclasses import dataclass
from typing import ClassVar, Final, Self

from app.config.objs.system import WormholeType

from .base.state_obj import BaseStateObj
from .base import PlayerOwnable

class _BaseSpecialTokenState(BaseStateObj, PlayerOwnable):

    def to_save_dict(self) -> dict:
        return PlayerOwnable.to_save_dict(self)

@dataclass(slots=True, kw_only=True)
class NaaluTokenState(_BaseSpecialTokenState):
    pass

@dataclass(slots=True, kw_only=True)
class SpeakerTokenState(_BaseSpecialTokenState):

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

    def to_save_dict(self) -> dict:
        return {
            "assimilated_faction_tech_id": self.assimilated_faction_tech_id
        }
    
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

    _VALID_WORMHOLE_TYPES: ClassVar[tuple[WormholeType, ...]] = (WormholeType.ALPHA, WormholeType.BETA)

    def __post_init__(self):
        if self.wormhole_type not in self._VALID_WORMHOLE_TYPES:
            raise InvalidWormholeType(f"Invalid wormhole type {self.wormhole_type} for Creuss token. Valid types are: {', '.join(t.name for t in self._VALID_WORMHOLE_TYPES)}")

    def to_save_dict(self) -> dict:
        return {
            "wormhole_type": self.wormhole_type.value,
            "active_system_id": self.active_system_id
        }

    @classmethod
    def from_save_dict(cls, wormhole_type: str, **kwargs) -> Self:
        return cls(
            wormhole_type=WormholeType(wormhole_type),
            **kwargs
        )

@dataclass(slots=True, kw_only=True)
class CustodiansTokenState(BaseStateObj):
    is_on_mecatol_rex: bool = True
