from dataclasses import dataclass

from app.config.shared import IDConfigObj

from app.geometry.coordinate import HexCoordinate

@dataclass(frozen=True)
class MapConfig(IDConfigObj):
    tiles: tuple[HexCoordinate, ...]
    