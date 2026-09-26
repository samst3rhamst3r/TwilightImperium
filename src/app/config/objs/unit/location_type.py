from enum import auto

from app.config.enum import SerializableEnum

class UnitLocationType(SerializableEnum):
    PLANET = auto()
    SYSTEM = auto()
    SHIP = auto()
