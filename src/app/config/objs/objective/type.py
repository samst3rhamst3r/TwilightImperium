from enum import auto

from app.config.shared.enum import ConfigEnum

class ObjectiveType(ConfigEnum):
    PUBLIC_STAGE_I = auto()
    PUBLIC_STAGE_II = auto()
    SECRET = auto()