from dataclasses import dataclass
from typing import Final, ClassVar, Self

from app.state.base import Serializable
from app.config.objs.system import WormholeType

class InvalidWormholeType(ValueError):
    pass

@dataclass(kw_only=True)
class CreussWormholeTokenState(Serializable):
    wormhole_type: Final[WormholeType]
    active_system_id: str | None = None

    _VALID_WORMHOLE_TYPES: ClassVar[tuple[WormholeType, ...]] = (WormholeType.ALPHA, WormholeType.BETA)

    @classmethod
    def new_game(cls) -> tuple[Self, Self]:
        return (
            cls(wormhole_type=WormholeType.ALPHA),
            cls(wormhole_type=WormholeType.BETA),
        )

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
