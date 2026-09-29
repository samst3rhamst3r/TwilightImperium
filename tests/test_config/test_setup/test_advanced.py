"""Mirrors src/app/config/setup/advanced.py."""
import pytest

from app.config.objs.system import TileColor
from app.config.setup import AdvancedMapSetupTileConfig, AdvancedSetupConfig, SetupConfig

def _tile(*, tile_color: TileColor = TileColor.BLUE, num_tiles: int = 1) -> AdvancedMapSetupTileConfig:
    return AdvancedMapSetupTileConfig(tile_color=tile_color, num_tiles=num_tiles)

def test_advanced_setup_is_composed_into_setup_config_not_inherited() -> None:
    """Every player count has an advanced variant, so it rides along as a
    `SetupConfig.advanced` field rather than a SetupConfig subclass."""
    assert not issubclass(AdvancedSetupConfig, SetupConfig)
    assert SetupConfig.__dataclass_fields__["advanced"].type is AdvancedSetupConfig

def test_advanced_setup_config_extra_tiles_defaults_to_empty() -> None:
    config = AdvancedSetupConfig(setup_tiles_per_player=(_tile(),))
    assert config.extra_setup_tiles == ()

def test_from_dict_builds_typed_tiles_and_defaults_extras() -> None:
    config = AdvancedSetupConfig.from_dict({"setup_tiles_per_player": [{"tile_color": "red", "num_tiles": 2}]})
    assert config.setup_tiles_per_player == (_tile(tile_color=TileColor.RED, num_tiles=2),)
    assert config.extra_setup_tiles == ()

@pytest.mark.parametrize("num_tiles", [0, -1])
def test_advanced_map_setup_tile_config_rejects_non_positive_tile_counts(num_tiles: int) -> None:
    with pytest.raises(ValueError):
        _tile(num_tiles=num_tiles)

def test_advanced_map_setup_tile_config_accepts_blue_and_red() -> None:
    assert _tile(tile_color=TileColor.BLUE).tile_color == TileColor.BLUE
    assert _tile(tile_color=TileColor.RED).tile_color == TileColor.RED

def test_advanced_map_setup_tile_config_rejects_green() -> None:
    """Real TI4 rule: the advanced map-assembly draw pool is only ever blue
    or red system tiles - green-backed systems (home systems) are never
    part of this pool, unlike TileColor's third member."""
    with pytest.raises(ValueError):
        _tile(tile_color=TileColor.GREEN)

def test_real_advanced_tiles_exactly_fill_the_map(setup_configs, map_configs) -> None:
    """Tiles dealt to players plus the pre-placed extras must fill every
    map hex except the home systems and Mecatol Rex - no more, no less."""
    for num_players, setup in setup_configs.items():
        advanced = setup.advanced
        dealt = num_players * sum(t.num_tiles for t in advanced.setup_tiles_per_player)
        extra = sum(t.num_tiles for t in advanced.extra_setup_tiles)
        open_hexes = len(map_configs[setup.map_shape_id].tiles) - num_players - 1  # homes + Mecatol Rex
        assert dealt + extra == open_hexes, (
            f"{num_players}-player advanced setup places {dealt} + {extra} tiles into {open_hexes} open hexes"
        )

def test_only_five_player_setup_has_extra_tiles(setup_configs) -> None:
    for num_players, setup in setup_configs.items():
        if num_players != 5:
            assert setup.advanced.extra_setup_tiles == (), f"{num_players}-player setup has extra tiles"
    assert setup_configs[5].advanced.extra_setup_tiles
