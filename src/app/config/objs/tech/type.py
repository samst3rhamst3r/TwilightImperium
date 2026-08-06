from enum import auto

from app.config.shared.enum import ConfigEnum

class TechType(ConfigEnum):
    BIOTIC = auto()
    WARFARE = auto()
    PROPULSION = auto()
    CYBERNETIC = auto()
