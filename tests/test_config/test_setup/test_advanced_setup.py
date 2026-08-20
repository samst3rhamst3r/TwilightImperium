"""Mirrors src/app/config/setup/advanced_setup.py.

Unlike test_setup.py, there is no real-data fixture to exercise here yet:
data/setup/advanced_setup.yaml exists, but no yaml_loader function parses it
into AdvancedSetupConfig/AdvancedMapSetupTileConfig instances (only
load_setup_data, which yields plain SetupConfig, is wired up so far). Until
that loader exists, these classes are only exercisable via direct
construction - loader coverage belongs in test_yaml_loader.py once it's
added.
"""
import pytest

from app.config.objs.system import TileColor
from app.config.setup import AdvancedMapSetupTileConfig, AdvancedSetupConfig, SetupConfig
from app.config.objs.map import MapShape

def _tile(*, tile_color: TileColor = TileColor.BLUE, num_tiles: int = 1) -> AdvancedMapSetupTileConfig:
    return AdvancedMapSetupTileConfig(tile_color=tile_color, num_tiles=num_tiles)

def test_advanced_setup_config_is_a_setup_config() -> None:
    """AdvancedSetupConfig extends SetupConfig (subclass split, not an
    optional field) - see ARCHITECTURE.md section 2's tech_type worked
    example, applied here to setup mode instead of tech."""
    assert issubclass(AdvancedSetupConfig, SetupConfig)

def test_advanced_setup_config_requires_no_player_setup_change() -> None:
    """AdvancedSetupConfig only adds tile-count data - it inherits
    map_shape_id/player_setup unchanged from SetupConfig."""
    config = AdvancedSetupConfig(
        map_shape_id=MapShape.STANDARD,
        player_setup=(),
        advanced_map_setup_tiles_per_player=(_tile(),),
    )
    assert config.map_shape_id == MapShape.STANDARD
    assert config.player_setup == ()

def test_advanced_setup_config_extra_tiles_defaults_to_empty() -> None:
    config = AdvancedSetupConfig(
        map_shape_id=MapShape.STANDARD,
        player_setup=(),
        advanced_map_setup_tiles_per_player=(_tile(),),
    )
    assert config.extra_advanced_map_setup_tiles == ()

@pytest.mark.parametrize("num_tiles", [0, -1])
def test_advanced_map_setup_tile_config_rejects_non_positive_tile_counts(num_tiles: int) -> None:
    with pytest.raises(ValueError):
        _tile(num_tiles=num_tiles)

def test_advanced_map_setup_tile_config_accepts_blue_and_red() -> None:
    assert _tile(tile_color=TileColor.BLUE).tile_color == TileColor.BLUE
    assert _tile(tile_color=TileColor.RED).tile_color == TileColor.RED

def test_advanced_map_setup_tile_config_rejects_green() -> None:
    """Real TI4 rule: the advanced/complete map-assembly draw pool is only
    ever blue (green/resource-heavy) or red (hazardous) system tiles -
    green-tile-class systems (home systems, Mecatol Rex) are never part of
    this pool, unlike TileColor's third member."""
    with pytest.raises(ValueError):
        _tile(tile_color=TileColor.GREEN)
