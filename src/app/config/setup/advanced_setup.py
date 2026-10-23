from dataclasses import dataclass

from app.config.shared import BaseConfigObj
from app.config.objs.system import TileColor

from .base import SetupConfig

@dataclass(frozen=True, kw_only=True)
class _AdvancedMapSetupTileConfig(BaseConfigObj):
    tile_color: TileColor
    num_tiles: int

    def __post_init__(self):
        if self.num_tiles < 1:
            raise ValueError(f"num_tiles must be at least 1, got {self.num_tiles}")
        elif self.tile_color not in [TileColor.BLUE, TileColor.RED]:
            raise ValueError(f"tile_color must be either BLUE or RED, got {self.tile_color}")

    @classmethod
    def _parse_fields(cls, d: dict) -> None:
        super()._parse_fields(d)
        d["tile_color"] = TileColor(d["tile_color"])

@dataclass(frozen=True, kw_only=True)
class AdvancedSetupConfig(SetupConfig):
    setup_tiles_per_player: tuple[_AdvancedMapSetupTileConfig, ...]
    extra_setup_tiles: tuple[_AdvancedMapSetupTileConfig, ...] = ()

    @classmethod
    def _parse_fields(cls, d: dict) -> None:
        super()._parse_fields(d)
        d["setup_tiles_per_player"] = tuple(_AdvancedMapSetupTileConfig.from_dict(tile_config) for tile_config in d["setup_tiles_per_player"])
        if d.get("extra_setup_tiles") is not None:
            d["extra_setup_tiles"] = tuple(_AdvancedMapSetupTileConfig.from_dict(tile_config) for tile_config in d["extra_setup_tiles"])
