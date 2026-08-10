"""Mirrors src/app/config/objs/objective/type.py."""
from app.config.objs.objective import ObjectiveType
from app.config.shared.enum import ConfigEnum

def test_objective_type_is_a_configenum() -> None:
    assert issubclass(ObjectiveType, ConfigEnum)

def test_objective_type_has_the_expected_members() -> None:
    assert {member.value for member in ObjectiveType} == {"public_stage_i", "public_stage_ii", "secret"}
