"""Mirrors src/app/config/objs/ability/parameterized/parameterized.py."""
from app.config.objs.ability import (
    AbilityConfig,
    ParameterizedAbilityConfig,
    ParameterizedAbilityPredicateType,
)
from app.config.objs.ability.parameterized.parameterized import (
    ParameterizedAbilityInstanceArgsConfig,
    ParameterizedAbilityPredicateConfig,
)

_RAW = {
    "id": "production",
    "name": "Production",
    "instance_args": {
        "predicate_type": "only_one_of",
        "predicates": [
            {"name": "value", "nullable": True, "required": False, "default": None, "min": 1},
            {"name": "amt_more_than_rsrc_value_of_planet", "nullable": True, "required": False, "default": None, "min": 1},
        ],
    },
}

def test_parameterized_ability_config_is_an_ability_config() -> None:
    assert issubclass(ParameterizedAbilityConfig, AbilityConfig)

def test_from_dict_builds_the_full_nested_shape() -> None:
    ability = ParameterizedAbilityConfig.from_dict(_RAW)
    assert isinstance(ability.instance_args, ParameterizedAbilityPredicateConfig)
    assert ability.instance_args.predicate_type is ParameterizedAbilityPredicateType.ONLY_ONE_OF
    assert isinstance(ability.instance_args.predicates, tuple)
    assert all(isinstance(p, ParameterizedAbilityInstanceArgsConfig) for p in ability.instance_args.predicates)
    assert [p.name for p in ability.instance_args.predicates] == ["value", "amt_more_than_rsrc_value_of_planet"]

def test_real_parameterized_abilities_have_at_least_one_predicate(ruleset_config) -> None:
    parameterized = [a for a in ruleset_config.abilities.values() if isinstance(a, ParameterizedAbilityConfig)]
    assert parameterized
    for ability in parameterized:
        assert ability.instance_args.predicates, f"{ability.id} declares no predicates"

def test_real_required_predicates_have_no_default(ruleset_config) -> None:
    """A required arg with a default is contradictory - the default could never apply."""
    for ability in ruleset_config.abilities.values():
        if isinstance(ability, ParameterizedAbilityConfig):
            for p in ability.instance_args.predicates:
                if p.required:
                    assert p.default is None, f"{ability.id}.{p.name} is required but has default {p.default!r}"
