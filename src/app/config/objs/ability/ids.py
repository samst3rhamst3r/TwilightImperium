from enum import auto

from app.config.enum.base import ConfigEnum

class AbilityID(ConfigEnum):
    BOMBARDMENT = auto()
    SUSTAIN_DAMAGE = auto()
    ANTI_FIGHTER_BARRAGE = auto()
    SPACE_CANNON = auto()
    PRODUCTION = auto()