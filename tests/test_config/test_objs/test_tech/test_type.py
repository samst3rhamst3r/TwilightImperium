"""Mirrors src/app/config/objs/tech/type.py."""
from app.config.objs.tech import TechType
from app.config.shared.enum import ConfigEnum

def test_tech_type_is_a_configenum() -> None:
    assert issubclass(TechType, ConfigEnum)

def test_tech_type_has_the_expected_members() -> None:
    assert {member.value for member in TechType} == {"biotic", "warfare", "propulsion", "cybernetic"}
