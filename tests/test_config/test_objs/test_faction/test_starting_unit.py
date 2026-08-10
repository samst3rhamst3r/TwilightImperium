"""Mirrors src/app/config/objs/faction/starting_unit.py."""
from app.config.objs.faction import FactionStartingUnitConfig
from app.config.objs.unit import UnitClass
from app.config.shared import BaseConfigObj

def test_faction_starting_unit_config_inherits_base_config_obj() -> None:
    assert issubclass(FactionStartingUnitConfig, BaseConfigObj)

def test_construction_with_a_real_unit_class() -> None:
    starting_unit = FactionStartingUnitConfig(unit_class=UnitClass.CARRIER, num=4)
    assert starting_unit.unit_class is UnitClass.CARRIER
    assert starting_unit.num == 4
