from dataclasses import dataclass

from app.geometry.coordinate import HexCoordinate

from .shared import BaseConfigObj, CanHaveFactionExclusivity
from .objs.map import MapShape

@dataclass(slots=True, frozen=True, kw_only=True)
class PlayerSetupConfig(BaseConfigObj):
    home_system_coordinates: HexCoordinate
    trade_good_bonus: int = 0

@dataclass(slots=True, frozen=True, kw_only=True)
class SetupConfig(CanHaveFactionExclusivity):
    map_shape_id: MapShape
    player_setup: tuple[PlayerSetupConfig, ...]