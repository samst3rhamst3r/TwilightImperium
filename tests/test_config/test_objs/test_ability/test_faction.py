"""Mirrors src/app/config/objs/ability/faction.py."""
import pytest

from app.config.objs.ability import AbilityConfig, FactionAbilityConfig
from app.config.objs.mixins import RequiresFactionExclusivity, RequiresFunctionalText

def test_faction_ability_config_composes_the_expected_mixins() -> None:
    assert issubclass(FactionAbilityConfig, AbilityConfig)
    assert issubclass(FactionAbilityConfig, RequiresFactionExclusivity)
    assert issubclass(FactionAbilityConfig, RequiresFunctionalText)

def test_faction_ability_requires_a_faction() -> None:
    with pytest.raises(TypeError):
        FactionAbilityConfig(id="x", name="X", functional_text="...")

def test_real_faction_abilities_have_text_and_a_real_faction(ruleset_config) -> None:
    faction_abilities = [a for a in ruleset_config.abilities.values() if isinstance(a, FactionAbilityConfig)]
    assert faction_abilities
    for ability in faction_abilities:
        assert ability.functional_text, f"{ability.id} has no functional_text"
        assert ability.faction_exclusive_id in ruleset_config.factions, (
            f"{ability.id} references unknown faction {ability.faction_exclusive_id!r}"
        )
