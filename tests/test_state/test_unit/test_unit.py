"""Tests for app.state.unit.unit.UnitState.

`location` is required, not Optional - a deployed unit always occupies
exactly one place on the board; a unit with no location has been destroyed
and removed from GameState.deployed_units entirely, never left behind with
location=None (see class docstring)."""
import pytest

from app.config.objs.unit import UnitLocationType
from app.state.unit.location import UnitLocation
from app.state.unit.unit import UnitState

@pytest.fixture
def unit_factory():
    def _make(**overrides) -> UnitState:
        defaults = {
            "config_id": "infantry",
            "location": UnitLocation(loc_type=UnitLocationType.SYSTEM, location_id="sys_18"),
        }
        return UnitState(**(defaults | overrides))
    return _make

def test_unit_state_requires_a_location() -> None:
    with pytest.raises(TypeError):
        UnitState(config_id="infantry")

def test_place_on_ship(unit_factory) -> None:
    unit = unit_factory()
    unit.place_on_ship("carrier-instance-id")
    assert unit.location.is_on_ship
    assert unit.location.location_id == "carrier-instance-id"

def test_place_on_planet(unit_factory) -> None:
    unit = unit_factory()
    unit.place_on_planet("mecatol_rex")
    assert unit.location.is_on_planet
    assert unit.location.location_id == "mecatol_rex"

def test_place_in_system(unit_factory) -> None:
    unit = unit_factory()
    unit.place_in_system("sys_25")
    assert unit.location.is_in_system
    assert unit.location.location_id == "sys_25"

def test_take_hit_and_repair(unit_factory) -> None:
    unit = unit_factory()
    unit.take_hit()
    assert unit.current_damage == 1
    unit.repair()
    assert unit.current_damage == 0

def test_repair_does_not_go_below_zero(unit_factory) -> None:
    unit = unit_factory()
    unit.repair()
    assert unit.current_damage == 0

def test_unit_state_save_load_round_trip(unit_factory, declared_immutable_field_violations) -> None:
    unit = unit_factory()
    unit.place_on_planet("mecatol_rex")
    unit.take_hit()

    reloaded = UnitState.load(unit.save())

    assert reloaded.config_id == unit.config_id
    assert reloaded.instance_id == unit.instance_id
    assert reloaded.current_damage == 1
    assert reloaded.location.loc_type is unit.location.loc_type
    assert reloaded.location.location_id == "mecatol_rex"
    assert not declared_immutable_field_violations(reloaded)
