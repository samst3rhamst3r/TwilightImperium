"""Mirrors src/app/config/objs/ability/base.py."""
from app.config.objs.ability import AbilityConfig
from app.config.objs.mixins import RequiresFunctionalText
from app.config.objs.named import NamedConfigObj

def test_ability_config_is_a_named_config_obj() -> None:
    assert issubclass(AbilityConfig, NamedConfigObj)

def test_base_ability_config_carries_no_functional_text() -> None:
    """Standard abilities (e.g. Sustain Damage) are rules-reference keywords
    - their behavior lives in code, not in per-card text."""
    assert not issubclass(AbilityConfig, RequiresFunctionalText)

def test_str_resolves_to_name_via_named_config_obj() -> None:
    ability = AbilityConfig(id="sustain_damage", name="Sustain Damage")
    assert str(ability) == "Sustain Damage"
