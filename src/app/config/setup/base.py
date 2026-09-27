from dataclasses import dataclass

from app.geometry.coordinate import HexCoordinate

from app.config import FromDictMixin
from app.config.objs.map import MapShape

from .advanced import AdvancedSetupConfig

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
    advanced: AdvancedSetupConfig

    @property
    def num_players(self) -> int:
        return len(self.player_setup)

    @classmethod
    def _init_from_dict(cls, d: dict) -> None:
        d["map_shape_id"] = MapShape(d["map_shape_id"])
        d["player_setup"] = tuple(PlayerSetupConfig.from_dict(player) for player in d["player_setup"])
        d["advanced"] = AdvancedSetupConfig.from_dict(d["advanced"])
