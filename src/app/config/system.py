from dataclasses import dataclass, field
from collections.abc import Sequence
from typing import Optional

from .shared.obj_ import ConfigObj, ConfigRefObj
from ..types.anomaly import Anomaly
from ..types.wormhole import Wormhole
from ..types.tile_color import TileColor

@dataclass(slots=True, frozen=True, kw_only=True)
class SystemConfig(ConfigObj):
    back_color: TileColor
    planets: Optional[Sequence[ConfigRefObj]] = field(default_factory=tuple)
    anomaly: Optional[Anomaly] = None
    wormhole: Optional[Wormhole] = None
