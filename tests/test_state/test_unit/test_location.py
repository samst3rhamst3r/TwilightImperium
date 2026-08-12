"""Tests for app.state.unit.location.UnitLocation.

`location_id` holds the *container's* id (system/planet/ship instance id)
for all three loc_type variants - only meaningfully "a unit's id" when
loc_type is SHIP (see field docstring/ARCHITECTURE.md review notes)."""
import pytest

from app.config.objs.unit import UnitLocationType
from app.state.unit.location import UnitLocation

def test_is_on_planet() -> None:
    loc = UnitLocation(loc_type=UnitLocationType.PLANET, location_id="mecatol_rex")
    assert loc.is_on_planet
    assert not loc.is_in_system
    assert not loc.is_on_ship

def test_is_in_system() -> None:
    loc = UnitLocation(loc_type=UnitLocationType.SYSTEM, location_id="sys_18")
    assert loc.is_in_system
    assert not loc.is_on_planet
    assert not loc.is_on_ship

def test_is_on_ship() -> None:
    loc = UnitLocation(loc_type=UnitLocationType.SHIP, location_id="some-ship-instance-id")
    assert loc.is_on_ship
    assert not loc.is_on_planet
    assert not loc.is_in_system

@pytest.mark.parametrize(
    "loc_type",
    [UnitLocationType.PLANET, UnitLocationType.SYSTEM, UnitLocationType.SHIP],
)
def test_unit_location_save_load_round_trip(loc_type) -> None:
    loc = UnitLocation(loc_type=loc_type, location_id="some-id")

    reloaded = UnitLocation.load(loc.save())

    assert reloaded.loc_type is loc_type
    assert reloaded.location_id == "some-id"
