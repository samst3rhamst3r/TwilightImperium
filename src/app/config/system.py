from dataclasses import dataclass, field
from collections.abc import Sequence
from typing import Optional

from .shared.obj_ import ConfigObj
from ..types.anomaly import Anomaly
from ..types.wormhole import Wormhole
from ..types.tile_color import TileColor

@dataclass(slots=True, frozen=True, kw_only=True)
class SystemConfig(ConfigObj):
    back_color: Optional[TileColor]
    planet_ids: Optional[Sequence[str]] = field(default_factory=tuple)
    anomaly: Optional[Anomaly] = None
    wormhole: Optional[Wormhole] = None
    home_faction_id: Optional[str] = None
    is_off_board: bool = False # Unique trait for Ghosts of Creuss
