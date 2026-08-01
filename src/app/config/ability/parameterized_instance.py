from dataclasses import dataclass
from typing import Optional

from app.config.shared import BaseConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class ParameterizedAbilityInstanceConfig(BaseConfigObj):
    ability_id: str

@dataclass(slots=True, frozen=True, kw_only=True)
class CombatAbilityInstanceConfig(ParameterizedAbilityInstanceConfig):
    combat: int
    dice: int = 1

@dataclass(slots=True, frozen=True, kw_only=True)
class ProductionAbilityInstanceConfig(ParameterizedAbilityInstanceConfig):
    value: Optional[int] = None
    amt_more_than_rsrc_value_of_planet: Optional[int] = None

    def __post_init__(self):
        if self.value is None and self.amt_more_than_rsrc_value_of_planet is None:
            raise ValueError("Either value or amt_more_than_rsrc_value_of_planet must be specified")
        if self.value is not None and self.amt_more_than_rsrc_value_of_planet is not None:
            raise ValueError("Only one of value or amt_more_than_rsrc_value_of_planet can be specified")

PARAMETERIZED_ABILITY_INSTANCE_REGISTRY = {
    "bombardment": CombatAbilityInstanceConfig,
    "anti_fighter_barrage": CombatAbilityInstanceConfig,
    "space_cannon": CombatAbilityInstanceConfig,
    "production": ProductionAbilityInstanceConfig
}