"""Mirrors src/app/config/objs/ability/ability.py."""
from app.config.objs.ability import AbilityConfig
from app.config.shared import CanHaveFactionExclusivity, NamedConfigObj, RequiresFunctionalText

def test_ability_config_composes_the_expected_mixins() -> None:
    assert issubclass(AbilityConfig, NamedConfigObj)
    assert issubclass(AbilityConfig, CanHaveFactionExclusivity)
    assert issubclass(AbilityConfig, RequiresFunctionalText)

def test_str_resolves_to_name_via_named_config_obj() -> None:
    ability = AbilityConfig(id="bombardment", name="Bombardment", functional_text="...")
    assert str(ability) == "Bombardment"

def test_real_ability_data_always_has_functional_text(ruleset_config) -> None:
    for ability in ruleset_config.abilities.values():
        assert ability.functional_text
