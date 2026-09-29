"""Mirrors src/app/config/objs/ability/parameterized/predicate_type.py."""
from app.config.enum import ConfigEnum
from app.config.objs.ability import ParameterizedAbilityPredicateType

def test_predicate_type_is_a_configenum() -> None:
    assert issubclass(ParameterizedAbilityPredicateType, ConfigEnum)

def test_predicate_type_has_the_expected_members() -> None:
    assert {m.value for m in ParameterizedAbilityPredicateType} == {"all_of", "only_one_of"}
