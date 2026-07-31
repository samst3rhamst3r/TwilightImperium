from dataclasses import dataclass
from typing import Optional

from .shared.obj_ import BaseConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class ParameterizedAbilityConfig(BaseConfigObj):
    ability_id: str

@dataclass(slots=True, frozen=True, kw_only=True)
class CombatAbilityConfig(ParameterizedAbilityConfig):
    combat: int
    dice: int = 1

@dataclass(slots=True, frozen=True, kw_only=True)
class ProductionAbilityConfig(ParameterizedAbilityConfig):
    value: Optional[int] = None
    amt_more_than_rsrc_value_of_planet: Optional[int] = None

    def __post_init__(self):
        if self.value is None and self.amt_more_than_rsrc_value_of_planet is None:
            raise ValueError("Either value or amt_more_than_rsrc_value_of_planet must be specified")
        if self.value is not None and self.amt_more_than_rsrc_value_of_planet is not None:
            raise ValueError("Only one of value or amt_more_than_rsrc_value_of_planet can be specified")

PARAMETERIZED_ABILITY_REGISTRY = {
    "bombardment": CombatAbilityConfig,
    "anti_fighter_barrage": CombatAbilityConfig,
    "space_cannon": CombatAbilityConfig,
    "production": ProductionAbilityConfig
}