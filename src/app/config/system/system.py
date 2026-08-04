from dataclasses import dataclass

from app.config.base import IDConfigObj

from .anomaly import AnomalyType
from .wormhole import WormholeType
from .tile_color import TileColor

@dataclass(slots=True, frozen=True, kw_only=True)
class SystemConfig(IDConfigObj):
    back_color: TileColor | None # Mecatol Rex is the sole exception of no tile back color. Field is still required to force explicit usage of None
    anomaly: AnomalyType | None = None
    wormhole: WormholeType | None = None
    is_off_board: bool = False # Unique trait for Ghosts of Creuss
