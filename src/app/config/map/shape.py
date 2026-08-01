from dataclasses import dataclass
from collections.abc import Sequence

from app.config.shared import BaseConfigObj

from .coordinate import HexCoordinate

@dataclass(slots=True, frozen=True, kw_only=True)
class MapShapeConfig(BaseConfigObj):
    coordinate_list: Sequence[HexCoordinate]
    