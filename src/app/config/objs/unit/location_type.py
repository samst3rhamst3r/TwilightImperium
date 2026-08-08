from enum import auto

from app.config.shared.enum import SerializableEnum

class UnitLocationType(SerializableEnum):
    PLANET = auto()
    SYSTEM = auto()
    SHIP = auto()
