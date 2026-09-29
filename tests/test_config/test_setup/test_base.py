"""Mirrors src/app/config/setup/base.py.

Real setup data is exercised via the ``setup_configs`` fixture
(tests/test_config/conftest.py), loaded directly via ``load_setup_data`` -
not via ``ruleset_config.setup``, which deliberately doesn't exist (see
ARCHITECTURE.md section 1 and
test_ruleset_config.py::test_ruleset_config_has_no_setup_field).
"""
from app.config.objs.map import MapShape
from app.config.setup import AdvancedSetupConfig, PlayerSetupConfig, SetupConfig
from app.geometry.coordinate import HexCoordinate

def test_player_setup_config_trade_good_bonus_defaults_to_zero() -> None:
    setup = PlayerSetupConfig(home_system_coordinates=HexCoordinate(0, 0))
    assert setup.trade_good_bonus == 0

def test_player_setup_from_dict_builds_a_hex_coordinate() -> None:
    setup = PlayerSetupConfig.from_dict({"home_system_coordinates": [3, -3], "trade_good_bonus": 2})
    assert setup.home_system_coordinates == HexCoordinate(3, -3)
    assert setup.trade_good_bonus == 2

def test_setup_config_from_dict_builds_the_full_nested_shape() -> None:
    setup = SetupConfig.from_dict({
        "map_shape_id": "triangular",
        "player_setup": [{"home_system_coordinates": [0, 0]}],
        "advanced": {"setup_tiles_per_player": [{"tile_color": "blue", "num_tiles": 1}]},
    })
    assert setup.map_shape_id is MapShape.TRIANGULAR
    assert setup.player_setup == (PlayerSetupConfig(home_system_coordinates=HexCoordinate(0, 0)),)
    assert isinstance(setup.advanced, AdvancedSetupConfig)
    assert setup.num_players == 1

def test_real_setup_num_players_matches_its_key(setup_configs) -> None:
    for num_players, setup in setup_configs.items():
        assert setup.num_players == num_players

def test_real_setup_data_covers_both_map_shapes(setup_configs) -> None:
    shapes = {setup.map_shape_id for setup in setup_configs.values()}
    assert shapes == {MapShape.STANDARD, MapShape.TRIANGULAR}

def test_real_home_coordinates_are_unique_and_on_the_map(setup_configs, map_configs) -> None:
    for num_players, setup in setup_configs.items():
        homes = [p.home_system_coordinates for p in setup.player_setup]
        assert len(set(homes)) == len(homes), f"{num_players}-player setup reuses a home coordinate"
        tiles = set(map_configs[setup.map_shape_id].tiles)
        off_map = [h for h in homes if h not in tiles]
        assert not off_map, f"{num_players}-player home coordinates not on the {setup.map_shape_id} map: {off_map}"

def test_only_five_player_setups_ever_grant_a_trade_good_bonus(setup_configs) -> None:
    """Real TI4 rule: trade good bonuses on starting positions only exist to
    balance 5-player games (an odd number of players around an otherwise
    symmetric map) - every other player count should be all zeros."""
    for num_players, setup in setup_configs.items():
        if num_players != 5:
            assert all(player.trade_good_bonus == 0 for player in setup.player_setup), (
                f"{setup.map_shape_id} setup with {num_players} players "
                "grants a trade good bonus, but only 5-player setups should"
            )
