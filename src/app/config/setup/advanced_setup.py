from dataclasses import dataclass

from app.config.shared import BaseConfigObj
from app.config.objs.system import TileColor

from .setup import SetupConfig

@dataclass(frozen=True, kw_only=True)
class AdvancedMapSetupTileConfig(BaseConfigObj):
    tile_color: TileColor
    num_tiles: int

    def __post_init__(self):
        if self.num_tiles < 1:
            raise ValueError(f"num_tiles must be at least 1, got {self.num_tiles}")
        elif self.tile_color not in [TileColor.BLUE, TileColor.RED]:
            raise ValueError(f"tile_color must be either BLUE or RED, got {self.tile_color}")

@dataclass(frozen=True, kw_only=True)
class AdvancedSetupConfig(SetupConfig):
    setup_tiles_per_player: tuple[AdvancedMapSetupTileConfig, ...]
    extra_setup_tiles: tuple[AdvancedMapSetupTileConfig, ...] = ()
