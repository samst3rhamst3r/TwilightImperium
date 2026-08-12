"""Tests for app.state.system.SystemState."""
from app.geometry import HexCoordinate
from app.state.system import SystemState

def test_system_state_save_load_round_trip() -> None:
    system = SystemState(config_id="sys_18", map_hex_coordinate=HexCoordinate(1, -1))

    reloaded = SystemState.load(system.save())

    assert reloaded.config_id == "sys_18"
    assert reloaded.map_hex_coordinate == HexCoordinate(1, -1)
