from enum import auto

from app.config.shared.enum import ConfigEnum

class AnomalyType(ConfigEnum):
    ASTEROID_FIELD = auto()
    NEBULA = auto()
    SUPERNOVA = auto()
    GRAVITY_RIFT = auto()
