from dataclasses import dataclass

from app.config.base import BaseConfigObj

from .coordinate import HexCoordinate

@dataclass(slots=True, frozen=True)
class MapShapeConfig(BaseConfigObj):
    coordinate_list: tuple[HexCoordinate, ...]
    