from dataclasses import dataclass

from app.geometry.coordinate import HexCoordinate

from app.config.shared import BaseConfigObj
from app.config.objs.map import MapShape

@dataclass(frozen=True, kw_only=True)
class _PlayerSetupConfig(BaseConfigObj):
    home_system_coordinates: HexCoordinate
    trade_good_bonus: int = 0

    @classmethod
    def _parse_fields(cls, d: dict) -> None:
        super()._parse_fields(d)
        d["home_system_coordinates"] = HexCoordinate(*d["home_system_coordinates"])

@dataclass(frozen=True, kw_only=True)
class SetupConfig(BaseConfigObj):
    map_shape_id: MapShape
    player_setup: tuple[_PlayerSetupConfig, ...]

    @classmethod
    def _parse_fields(cls, d: dict) -> None:
        super()._parse_fields(d)
        d["map_shape_id"] = MapShape(d["map_shape_id"])
        d["player_setup"] = tuple(_PlayerSetupConfig.from_dict(player_setup) for player_setup in d["player_setup"])
