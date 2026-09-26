from dataclasses import dataclass

from app.config.fromdict import FromDictMixin
from config.objs.ability.base import AbilityConfig

from .predicate_type import ParameterizedAbilityPredicateType

@dataclass(frozen=True, kw_only=True)
class ParameterizedAbilityInstanceArgsConfig:
    name: str
    nullable: bool
    required: bool
    default: int | None
    min: int

@dataclass(frozen=True, kw_only=True)
class ParameterizedAbilityPredicateConfig(FromDictMixin):
    predicate_type: ParameterizedAbilityPredicateType
    predicates: tuple[ParameterizedAbilityInstanceArgsConfig, ...]

    @classmethod
    def _init_from_dict(cls, d: dict) -> None:
        d["predicate_type"] = ParameterizedAbilityPredicateType(d["predicate_type"])
        d["predicates"] = tuple(ParameterizedAbilityInstanceArgsConfig(**arg) for arg in d["predicates"])

@dataclass(frozen=True, kw_only=True)
class ParameterizedAbilityConfig(AbilityConfig, FromDictMixin):
    instance_args: ParameterizedAbilityPredicateConfig

    @classmethod
    def _init_from_dict(cls, d: dict) -> None:
        d["instance_args"] = ParameterizedAbilityPredicateConfig.from_dict(d["instance_args"])