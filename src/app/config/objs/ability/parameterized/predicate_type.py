from app.config.enum import ConfigEnum
from enum import auto

class ParameterizedAbilityPredicateType(ConfigEnum):
    ALL_OF = auto()
    ONLY_ONE_OF = auto()
