from dataclasses import dataclass

from app.geometry.coordinate import HexCoordinate

from app.config import FromDictMixin
from app.config.objs.map import MapShape

@dataclass(frozen=True, kw_only=True)
class PlayerSetupConfig(FromDictMixin):
    home_system_coordinates: HexCoordinate
    trade_good_bonus: int = 0

    @classmethod
    def _init_from_dict(cls, d: dict) -> None:
        # Validate that the home_system_coordinates is a valid HexCoordinate
        d["home_system_coordinates"] = HexCoordinate(*d["home_system_coordinates"])

@dataclass(frozen=True, kw_only=True)
class SetupConfig(FromDictMixin):
    map_shape_id: MapShape
    player_setup: tuple[PlayerSetupConfig, ...]

    @classmethod
    def _init_from_dict(cls, d: dict) -> None:
        d["map_shape_id"] = MapShape(d["map_shape_id"])
        d["player_setup"] = tuple(PlayerSetupConfig.from_dict(player) for player in d["player_setup"])
