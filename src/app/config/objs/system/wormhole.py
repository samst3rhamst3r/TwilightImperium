from enum import auto

from app.config.enum.base import ConfigEnum

class WormholeType(ConfigEnum):
    ALPHA = auto()
    BETA = auto()
    DELTA = auto()
