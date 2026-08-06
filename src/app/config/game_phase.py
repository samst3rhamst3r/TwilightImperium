from enum import auto

from app.config.shared.enum import ConfigEnum

class GamePhase(ConfigEnum):
    STRATEGY = auto()
    ACTION = auto()
    STATUS = auto()
    AGENDA = auto()
