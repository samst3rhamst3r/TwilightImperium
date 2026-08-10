"""Mirrors src/app/config/objs/ability/ids.py."""
from app.config.objs.ability import AbilityID
from app.config.shared.enum import ConfigEnum

def test_ability_id_is_a_configenum() -> None:
    assert issubclass(AbilityID, ConfigEnum)

def test_ability_id_has_the_expected_members() -> None:
    assert {member.value for member in AbilityID} == {
        "bombardment", "sustain_damage", "anti_fighter_barrage", "space_cannon", "production",
    }
