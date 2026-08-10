"""Mirrors src/app/config/objs/tech/ids.py."""
from app.config.objs.tech import TechID
from app.config.shared.enum import ConfigEnum

def test_tech_id_is_a_configenum() -> None:
    assert issubclass(TechID, ConfigEnum)

def test_tech_id_has_the_expected_members() -> None:
    assert {member.value for member in TechID} == {"valefar_assimilator_x", "valefar_assimilator_y"}

def test_real_tech_data_contains_both_assimilator_ids(ruleset_config) -> None:
    assert TechID.VALEFAR_ASSIMILATOR_X in ruleset_config.techs
    assert TechID.VALEFAR_ASSIMILATOR_Y in ruleset_config.techs
