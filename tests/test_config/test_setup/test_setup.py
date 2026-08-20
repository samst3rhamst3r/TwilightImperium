"""Mirrors src/app/config/setup/setup.py.

Real setup data is exercised via the ``setup_configs`` fixture
(tests/test_config/conftest.py), loaded directly from
``yaml_loader.load_setup_data`` - not via ``ruleset_config.setup``, which
deliberately doesn't exist (see ARCHITECTURE.md section 1 and
test_ruleset_config.py::test_ruleset_config_has_no_setup_field).
"""
from app.config.objs.map import MapShape
from app.config.setup import PlayerSetupConfig, SetupConfig
from app.config.shared import BaseConfigObj
from app.geometry.coordinate import HexCoordinate

def test_setup_config_classes_inherit_base_config_obj() -> None:
    assert issubclass(PlayerSetupConfig, BaseConfigObj)
    assert issubclass(SetupConfig, BaseConfigObj)

def test_player_setup_config_trade_good_bonus_defaults_to_zero() -> None:
    setup = PlayerSetupConfig(home_system_coordinates=HexCoordinate(0, 0))
    assert setup.trade_good_bonus == 0

def test_real_setup_data_covers_both_map_shapes(setup_configs) -> None:
    shapes = {setup.map_shape_id for setup in setup_configs}
    assert shapes == {MapShape.STANDARD, MapShape.TRIANGULAR}

def test_real_setup_data_has_multiple_player_count_variants_per_shape(setup_configs) -> None:
    """This is exactly why load_setup_data returns a tuple rather than an
    id-keyed mapping - map_shape_id alone isn't unique."""
    standard_variants = [s for s in setup_configs if s.map_shape_id == MapShape.STANDARD]
    assert len({len(s.player_setup) for s in standard_variants}) > 1

def test_only_five_player_setups_ever_grant_a_trade_good_bonus(setup_configs) -> None:
    """Real TI4 rule: trade good bonuses on starting positions only exist to
    balance 5-player games (an odd number of players around an otherwise
    symmetric map) - every other player count should be all zeros."""
    for setup in setup_configs:
        if len(setup.player_setup) != 5:
            assert all(player.trade_good_bonus == 0 for player in setup.player_setup), (
                f"{setup.map_shape_id} setup with {len(setup.player_setup)} players "
                "grants a trade good bonus, but only 5-player setups should"
            )
