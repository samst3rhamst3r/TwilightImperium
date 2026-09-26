from enum import auto

from app.config.enum.base import ConfigEnum

class UnitClass(ConfigEnum):
    CARRIER = auto()
    CRUISER = auto()
    DESTROYER = auto()
    DREADNOUGHT = auto()
    FLAGSHIP = auto()
    FIGHTER = auto()
    INFANTRY = auto()
    PDS = auto()
    SPACE_DOCK = auto()
    WAR_SUN = auto()
