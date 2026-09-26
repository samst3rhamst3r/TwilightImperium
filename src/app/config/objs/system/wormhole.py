from enum import auto

from app.config.enum import ConfigEnum

class WormholeType(ConfigEnum):
    ALPHA = auto()
    BETA = auto()
    DELTA = auto()
