"""Mirrors src/app/config/objs/ability/parameterized/instance.py."""
from types import MappingProxyType

import pytest

from app.config.objs.ability import ParameterizedAbilityConfig, ParameterizedAbilityInstanceConfig

def test_from_dict_freezes_instance_args() -> None:
    instance = ParameterizedAbilityInstanceConfig.from_dict(
        {"ability_id": "bombardment", "instance_args": {"combat": 5, "dice": 3}}
    )
    assert isinstance(instance.instance_args, MappingProxyType)
    assert dict(instance.instance_args) == {"combat": 5, "dice": 3}
    with pytest.raises(TypeError):
        instance.instance_args["combat"] = 1

def test_real_unit_instances_reference_real_parameterized_abilities(ruleset_config) -> None:
    instances = [i for unit in ruleset_config.units.values() for i in unit.parameterized_abilities]
    assert instances, "expected at least one unit with a parameterized ability in real data"
    for instance in instances:
        assert isinstance(ruleset_config.abilities.get(instance.ability_id), ParameterizedAbilityConfig), (
            f"{instance.ability_id!r} is not a known parameterized ability"
        )

def test_real_unit_instance_args_are_declared_by_their_ability(ruleset_config) -> None:
    """Every key a unit passes must be a predicate its ability declares -
    a mistyped arg name in units.yaml should fail here, not at game time."""
    for unit in ruleset_config.units.values():
        for instance in unit.parameterized_abilities:
            ability = ruleset_config.abilities[instance.ability_id]
            declared = {p.name for p in ability.instance_args.predicates}
            unknown = instance.instance_args.keys() - declared
            assert not unknown, f"{unit.id}: {instance.ability_id} got undeclared args {sorted(unknown)}"
