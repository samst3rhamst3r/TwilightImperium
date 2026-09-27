from dataclasses import dataclass

from app.config import FromDictMixin
from app.config.objs.system import TileColor

@dataclass(frozen=True, kw_only=True)
class AdvancedMapSetupTileConfig(FromDictMixin):
    tile_color: TileColor
    num_tiles: int

    @classmethod
    def _init_from_dict(cls, d: dict) -> None:
        d["tile_color"] = TileColor(d["tile_color"])

    def __post_init__(self):
        if self.num_tiles < 1:
            raise ValueError(f"num_tiles must be at least 1, got {self.num_tiles}")
        elif self.tile_color not in [TileColor.BLUE, TileColor.RED]:
            raise ValueError(f"tile_color must be either BLUE or RED, got {self.tile_color}")

@dataclass(frozen=True, kw_only=True)
class AdvancedSetupConfig(FromDictMixin):
    setup_tiles_per_player: tuple[AdvancedMapSetupTileConfig, ...]
    extra_setup_tiles: tuple[AdvancedMapSetupTileConfig, ...] = ()

    @classmethod
    def _init_from_dict(cls, d: dict) -> None:
        super()._init_from_dict(d)
        d["setup_tiles_per_player"] = tuple(AdvancedMapSetupTileConfig.from_dict(tile) for tile in d["setup_tiles_per_player"])
        d["extra_setup_tiles"] = tuple(AdvancedMapSetupTileConfig.from_dict(tile) for tile in d.get("extra_setup_tiles", ()))
