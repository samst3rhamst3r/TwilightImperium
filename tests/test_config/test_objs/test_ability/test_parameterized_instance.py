"""Mirrors src/app/config/objs/ability/parameterized_instance.py."""
import pytest

from app.config.objs.ability.ids import AbilityID
from app.config.objs.ability.parameterized_instance import (
    CombatAbilityInstanceConfig,
    ParameterizedAbilityInstanceConfig,
    ProductionAbilityInstanceConfig,
)
from app.config.shared import IDConfigObj

def test_parameterized_ability_instance_config_inherits_id_config_obj() -> None:
    assert issubclass(ParameterizedAbilityInstanceConfig, IDConfigObj)

@pytest.mark.parametrize("id_value", [AbilityID.BOMBARDMENT, "bombardment"], ids=["enum", "str"])
def test_id_field_accepts_either_the_ability_id_enum_or_its_raw_string(id_value) -> None:
    """id is a plain `str` field (IDConfigObj.id: str) with no ConfigEnum
    coercion of its own - AbilityID is a StrEnum, so passing the enum member
    directly still behaves like the plain string everywhere it matters."""
    combat = CombatAbilityInstanceConfig(id=id_value, combat=5)
    assert combat.id == "bombardment"
    assert isinstance(combat.id, str)

def test_combat_ability_instance_config_dice_defaults_to_one() -> None:
    combat = CombatAbilityInstanceConfig(id=AbilityID.BOMBARDMENT, combat=5)
    assert combat.dice == 1

def test_production_ability_instance_config_rejects_neither_value_kind_given() -> None:
    with pytest.raises(ValueError):
        ProductionAbilityInstanceConfig(id=AbilityID.PRODUCTION)

def test_production_ability_instance_config_rejects_both_value_kinds_given() -> None:
    with pytest.raises(ValueError):
        ProductionAbilityInstanceConfig(id=AbilityID.PRODUCTION, value=1, amt_more_than_rsrc_value_of_planet=1)

def test_production_ability_instance_config_accepts_either_value_kind_alone() -> None:
    assert ProductionAbilityInstanceConfig(id=AbilityID.PRODUCTION, value=3).value == 3
    assert (
        ProductionAbilityInstanceConfig(id=AbilityID.PRODUCTION, amt_more_than_rsrc_value_of_planet=1)
        .amt_more_than_rsrc_value_of_planet
        == 1
    )
