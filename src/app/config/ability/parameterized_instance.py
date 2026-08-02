from dataclasses import dataclass

from app.config.base import BaseConfigObj

from .ids import AbilityID

@dataclass(slots=True, frozen=True, kw_only=True)
class ParameterizedAbilityInstanceConfig(BaseConfigObj):
    ability_id: AbilityID

@dataclass(slots=True, frozen=True, kw_only=True)
class CombatAbilityInstanceConfig(ParameterizedAbilityInstanceConfig):
    combat: int
    dice: int = 1

@dataclass(slots=True, frozen=True, kw_only=True)
class ProductionAbilityInstanceConfig(ParameterizedAbilityInstanceConfig):
    value: int | None = None
    amt_more_than_rsrc_value_of_planet: int | None = None

    def __post_init__(self):
        if self.value is None and self.amt_more_than_rsrc_value_of_planet is None:
            raise ValueError("Either value or amt_more_than_rsrc_value_of_planet must be specified")
        if self.value is not None and self.amt_more_than_rsrc_value_of_planet is not None:
            raise ValueError("Only one of value or amt_more_than_rsrc_value_of_planet can be specified")
