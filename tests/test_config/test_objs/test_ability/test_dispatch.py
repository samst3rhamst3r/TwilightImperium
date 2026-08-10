"""Mirrors src/app/config/objs/ability/dispatch.py."""
from app.config.objs.ability.dispatch import PARAMETERIZED_ABILITY_INSTANCE_REGISTRY
from app.config.objs.ability.ids import AbilityID
from app.config.objs.ability.parameterized_instance import ParameterizedAbilityInstanceConfig

def test_every_registry_key_is_an_ability_id() -> None:
    for key in PARAMETERIZED_ABILITY_INSTANCE_REGISTRY:
        assert isinstance(key, AbilityID)

def test_every_registry_value_is_a_parameterized_ability_instance_config_subclass() -> None:
    for value in PARAMETERIZED_ABILITY_INSTANCE_REGISTRY.values():
        assert issubclass(value, ParameterizedAbilityInstanceConfig)
