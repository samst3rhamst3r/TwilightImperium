from dataclasses import dataclass
from typing import ClassVar, Final

from app.config.objs.system import WormholeType
from app.state.base.ownable import PlayerOwnableWithConvenienceProtocol, PlayerOwnableMixin

from .base.serializable import Serializable

@dataclass(slots=True, kw_only=True)
class NaaluTokenState(PlayerOwnableWithConvenienceProtocol):
    pass

@dataclass(slots=True, kw_only=True)
class SpeakerTokenState(PlayerOwnableMixin):

    def assign_speaker(self, player_id: str) -> None:
        self.ownable.assign_owner(player_id)

    def reassign_speaker(self, player_id: str) -> str:
        return self.ownable.reassign_owner(player_id)

    def release_speaker(self) -> str:
        return self.ownable.release_owner()

    def is_player_speaker(self, player_id: str) -> bool:
        return self.ownable.is_owned_by_player(player_id)

    @property
    def speaker_player_id(self) -> str | None:
        return self.ownable.owned_by_player_id

@dataclass(slots=True, kw_only=True)
class NekroAssimilatorTokenState(Serializable):
    assimilated_faction_tech_id: str | None = None

    def save(self) -> dict:
        return super().save() | {
            "assimilated_faction_tech_id": self.assimilated_faction_tech_id
        }
    
    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        self.assimilated_faction_tech_id = data["assimilated_faction_tech_id"]

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
class CreussWormholeTokenState(Serializable):
    wormhole_type: Final[WormholeType]
    active_system_id: str | None = None

    _VALID_WORMHOLE_TYPES: ClassVar[tuple[WormholeType, ...]] = (WormholeType.ALPHA, WormholeType.BETA)

    def __post_init__(self):
        if self.wormhole_type not in self._VALID_WORMHOLE_TYPES:
            raise InvalidWormholeType(f"Invalid wormhole type {self.wormhole_type} for Creuss token. Valid types are: {', '.join(t.name for t in self._VALID_WORMHOLE_TYPES)}")

    def save(self) -> dict:
        return super().save() | {
            "wormhole_type": self.wormhole_type.value,
            "active_system_id": self.active_system_id
        }

    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        self.wormhole_type = WormholeType(data["wormhole_type"])
        self.active_system_id = data["active_system_id"]

@dataclass(slots=True, kw_only=True)
class CustodiansTokenState(Serializable):
    is_on_mecatol_rex: bool = True

    def save(self) -> dict:
        return super().save() | {
            "is_on_mecatol_rex": self.is_on_mecatol_rex
        }

    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        self.is_on_mecatol_rex = data["is_on_mecatol_rex"]
