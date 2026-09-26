from enum import auto

from app.config.enum.base import ConfigEnum

class TechType(ConfigEnum):
    BIOTIC = auto()
    WARFARE = auto()
    PROPULSION = auto()
    CYBERNETIC = auto()
