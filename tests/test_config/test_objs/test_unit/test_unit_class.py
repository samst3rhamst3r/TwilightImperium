"""Mirrors src/app/config/objs/unit/unit_class.py."""
from app.config.objs.unit import UnitClass
from app.config.shared.enum import ConfigEnum

def test_unit_class_is_a_configenum() -> None:
    assert issubclass(UnitClass, ConfigEnum)

def test_unit_class_has_the_ten_expected_members() -> None:
    assert {member.value for member in UnitClass} == {
        "carrier", "cruiser", "destroyer", "dreadnought", "flagship",
        "fighter", "infantry", "pds", "space_dock", "war_sun",
    }
