from enum import auto

from app.config.enum import ConfigEnum

class ObjectiveType(ConfigEnum):
    STAGE_I = auto()
    STAGE_II = auto()
    SECRET = auto()