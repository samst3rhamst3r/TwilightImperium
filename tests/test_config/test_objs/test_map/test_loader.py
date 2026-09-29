"""Mirrors src/app/config/objs/map/loader.py."""
import pytest

from app.config.objs.map import MapConfig, MapShape, load_first_game_system_tile_mapping, load_map_data

_PLAYER_COUNTS = (3, 4, 5, 6)

@pytest.mark.parametrize("shape", list(MapShape), ids=str)
def test_load_map_data_loads_one_map_per_shape(data_dir, shape: MapShape) -> None:
    map_config = load_map_data(data_dir, shape)
    assert isinstance(map_config, MapConfig)
    assert map_config.id == shape

@pytest.mark.parametrize("num_players", _PLAYER_COUNTS)
def test_first_game_mapping_length_matches_its_map_shape(
    data_dir, setup_configs, map_configs, num_players: int
) -> None:
    """The mapping is zipped positionally against MapConfig.tiles (see
    game_setup_session.py), so it must be exactly as long as the map that
    this player count's SetupConfig uses."""
    shape = setup_configs[num_players].map_shape_id
    mapping = load_first_game_system_tile_mapping(data_dir, num_players)
    assert len(mapping) == len(map_configs[shape].tiles)

@pytest.mark.parametrize("num_players", _PLAYER_COUNTS)
def test_first_game_mapping_non_null_entries_are_real_system_ids(
    data_dir, ruleset_config, num_players: int
) -> None:
    mapping = load_first_game_system_tile_mapping(data_dir, num_players)
    non_null = [system_id for system_id in mapping if system_id is not None]
    assert non_null, f"expected at least one placed system in the {num_players}-player mapping"
    for system_id in non_null:
        assert system_id in ruleset_config.systems, (
            f"{num_players}-player first-game mapping references unknown system id {system_id!r}"
        )

@pytest.mark.parametrize("num_players", _PLAYER_COUNTS)
def test_first_game_mapping_has_no_duplicate_system_placements(data_dir, num_players: int) -> None:
    mapping = load_first_game_system_tile_mapping(data_dir, num_players)
    non_null = [system_id for system_id in mapping if system_id is not None]
    duplicates = {system_id for system_id in non_null if non_null.count(system_id) > 1}
    assert not duplicates, f"{num_players}-player mapping places the same system twice: {duplicates}"
