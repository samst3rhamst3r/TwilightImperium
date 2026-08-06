from .ids import AbilityID
from .parameterized_instance import (CombatAbilityInstanceConfig, ProductionAbilityInstanceConfig)

PARAMETERIZED_ABILITY_INSTANCE_REGISTRY = {
    AbilityID.BOMBARDMENT: CombatAbilityInstanceConfig,
    AbilityID.ANTI_FIGHTER_BARRAGE: CombatAbilityInstanceConfig,
    AbilityID.SPACE_CANNON: CombatAbilityInstanceConfig,
    AbilityID.PRODUCTION: ProductionAbilityInstanceConfig
}