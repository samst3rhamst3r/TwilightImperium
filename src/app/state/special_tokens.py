from dataclasses import dataclass
from typing import ClassVar, Final, Literal, get_args, get_type_hints

from app.config.objs.system import WormholeType
from app.state.base.ownable import PlayerOwnableMixin
from app.state.base.mixins import ConfigIDStateObj

from .base.serializable import Serializable

@dataclass(kw_only=True)
class NaaluTokenState(PlayerOwnableMixin):
    pass

@dataclass(kw_only=True)
class SpeakerTokenState(PlayerOwnableMixin):

    def assign_speaker(self, player_id: str) -> None:
        self.ownable.set_owner(player_id)

    def release_speaker(self) -> str:
        return self.ownable.release_owner()

    @property
    def speaker_player_id(self) -> str | None:
        return self.ownable.owned_by_player_id

    @property
    def is_speaker_assigned(self) -> bool:
        return self.ownable.is_owned

    def is_player_speaker(self, player_id: str) -> bool:
        return self.ownable.is_owned_by_player(player_id)

@dataclass(kw_only=True)
class NekroAssimilatorTokenState(ConfigIDStateObj):
    """One of the two Valefar Assimilator tokens (config_id identifies X vs Y -
    see TechID.VALEFAR_ASSIMILATOR_X/_Y, ARCHITECTURE.md section 2)."""
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

@dataclass(kw_only=True)
class CreussWormholeTokenState(Serializable):
    wormhole_type: Final[Literal[WormholeType.ALPHA, WormholeType.BETA]]
    active_system_id: str | None = None

    def __post_init__(self):
        if self.wormhole_type not in (WormholeType.ALPHA, WormholeType.BETA):
            raise InvalidWormholeType(f"Invalid wormhole type {self.wormhole_type} for Creuss token. Valid types are: {', '.join(t.name for t in (WormholeType.ALPHA, WormholeType.BETA))}")

    def save(self) -> dict:
        return super().save() | {
            "wormhole_type": self.wormhole_type.value,
            "active_system_id": self.active_system_id
        }

    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        self.wormhole_type = WormholeType(data["wormhole_type"])
        self.active_system_id = data["active_system_id"]

@dataclass(kw_only=True)
class CustodiansTokenState(Serializable):
    is_on_mecatol_rex: bool = True

    def save(self) -> dict:
        return super().save() | {
            "is_on_mecatol_rex": self.is_on_mecatol_rex
        }

    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        self.is_on_mecatol_rex = data["is_on_mecatol_rex"]
