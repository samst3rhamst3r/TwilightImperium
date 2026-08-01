from dataclasses import dataclass
from typing import Optional

from app.config.base import ConfigObj

from .anomaly import Anomaly
from .wormhole import Wormhole
from .tile_color import TileColor

@dataclass(slots=True, frozen=True, kw_only=True)
class SystemConfig(ConfigObj):
    back_color: TileColor | None # Mecatol Rex is the sole exception of no tile back color
    anomaly: Optional[Anomaly] = None
    wormhole: Optional[Wormhole] = None
    is_off_board: bool = False # Unique trait for Ghosts of Creuss
