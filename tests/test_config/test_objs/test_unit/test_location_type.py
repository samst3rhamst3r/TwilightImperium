"""Mirrors src/app/config/objs/unit/location_type.py."""
from app.config.objs.unit import UnitLocationType
from app.config.shared.enum import ConfigEnum, SerializableEnum

def test_unit_location_type_is_not_a_configenum() -> None:
    """UnitLocationType is derived/internal (used by valid_locations.py to
    describe where a unit class may sit), never parsed directly out of a
    YAML value - so it's plain SerializableEnum, not ConfigEnum."""
    assert issubclass(UnitLocationType, SerializableEnum)
    assert not issubclass(UnitLocationType, ConfigEnum)

def test_unit_location_type_has_the_three_expected_members() -> None:
    assert {member.value for member in UnitLocationType} == {"planet", "system", "ship"}
