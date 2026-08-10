from dataclasses import dataclass

from app.geometry.coordinate import HexCoordinate

from .shared import BaseConfigObj
from .objs.map import MapShape

@dataclass(frozen=True, kw_only=True)
class PlayerSetupConfig(BaseConfigObj):
    home_system_coordinates: HexCoordinate
    trade_good_bonus: int = 0

@dataclass(frozen=True, kw_only=True)
class SetupConfig(BaseConfigObj):
    map_shape_id: MapShape
    player_setup: tuple[PlayerSetupConfig, ...]