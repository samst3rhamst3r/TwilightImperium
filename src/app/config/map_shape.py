from dataclasses import dataclass

from app.config.base import IDConfigObj

from app.geometry.coordinate import HexCoordinate

@dataclass(slots=True, frozen=True)
class MapShapeConfig(IDConfigObj):
    tiles: tuple[HexCoordinate, ...]
    