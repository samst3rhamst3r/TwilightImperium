from enum import auto

from app.config.enum import ConfigEnum

class Anomaly(ConfigEnum):
    ASTEROID_FIELD = auto()
    NEBULA = auto()
    SUPERNOVA = auto()
    GRAVITY_RIFT = auto()
