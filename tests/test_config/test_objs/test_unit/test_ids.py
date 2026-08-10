"""Mirrors src/app/config/objs/unit/ids.py."""
from app.config.objs.unit import UnitID
from app.config.shared.enum import ConfigEnum

def test_unit_id_is_a_configenum() -> None:
    assert issubclass(UnitID, ConfigEnum)

def test_unit_id_has_the_expected_members() -> None:
    assert {member.value for member in UnitID} == {"floating_factory_i", "floating_factory_ii"}

def test_real_unit_data_contains_both_floating_factory_ids(ruleset_config) -> None:
    assert UnitID.FLOATING_FACTORY_I in ruleset_config.units
    assert UnitID.FLOATING_FACTORY_II in ruleset_config.units
