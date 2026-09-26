from .base import AbilityConfig
from .faction import FactionAbilityConfig
from .parameterized import ParameterizedAbilityConfig, ParameterizedAbilityInstanceConfig, ParameterizedAbilityPredicateType

def load_ability_config(data: dict) -> AbilityConfig:
    if "faction_exclusive_id" in data:
        return FactionAbilityConfig(**data)
    elif "instance_args" in data:
        return ParameterizedAbilityConfig.from_dict(data)
    else:
        return AbilityConfig(**data)

def load_parameterized_ability_instance(data: dict, config_ref: ParameterizedAbilityConfig) -> ParameterizedAbilityInstanceConfig:

    if data["ability_id"] != config_ref.id:
        raise ValueError(f"Ability ID mismatch: {data['ability_id']} != {config_ref.id}")

    instance_args = data["instance_args"]

    config_args = config_ref.instance_args
    for config_arg in config_args.predicates:
        if config_arg.required and config_arg.name not in instance_args:
            raise ValueError(f"Missing required instance arg: {config_arg.name}")
        elif config_arg.name not in instance_args:
            instance_args[config_arg.name] = config_arg.default

        if instance_args[config_arg.name] is None and not config_arg.nullable:
            raise ValueError(f"Instance arg {config_arg.name} cannot be None. Set default to a value or set nullable to True if None is acceptable.")

        if instance_args[config_arg.name] is not None and instance_args[config_arg.name] < config_arg.min:
            raise ValueError(f"Instance arg {config_arg.name} must be at least {config_arg.min}")

    instance = ParameterizedAbilityInstanceConfig.from_dict(data)

    num_non_null_args = sum(1 for v in instance.instance_args.values() if v is not None)

    predicate_type = config_ref.instance_args.predicate_type
    if predicate_type == ParameterizedAbilityPredicateType.ALL_OF and len(instance.instance_args) != num_non_null_args:
        raise ValueError(f"Instance args must include all of the following: {[arg.name for arg in config_args.predicates]}")
    elif predicate_type == ParameterizedAbilityPredicateType.ONLY_ONE_OF and num_non_null_args != 1:
        raise ValueError(f"Instance args must include exactly one of the following: {[arg.name for arg in config_args.predicates]}")

    return instance