from enum import auto

from app.config.enum.base import SerializableEnum

class UnitLocationType(SerializableEnum):
    PLANET = auto()
    SYSTEM = auto()
    SHIP = auto()
