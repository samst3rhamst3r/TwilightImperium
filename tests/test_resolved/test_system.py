"""Tests for app.resolved.system.ResolvedSystem."""
from app.config.ruleset_config import RulesetConfig
from app.geometry import HexCoordinate
from app.resolved.system import ResolvedSystem
from app.state.system import SystemState

def test_resolved_system_binds_state_and_config(ruleset_config: RulesetConfig) -> None:
    system_state = SystemState(config_id="01", map_hex_coordinate=HexCoordinate(0, 0))
    system_config = ruleset_config.systems["01"]

    resolved = ResolvedSystem(system_state, system_config)

    assert resolved.state is system_state
    assert resolved.config is system_config
    assert resolved.config.id == "01"
