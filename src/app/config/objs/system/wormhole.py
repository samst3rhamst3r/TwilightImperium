from enum import auto

from app.config.shared.enum import ConfigEnum

class WormholeType(ConfigEnum):
    ALPHA = auto()
    BETA = auto()
    DELTA = auto()
