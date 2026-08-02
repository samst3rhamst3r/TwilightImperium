from enum import auto

from app.config.enum import ConfigEnum

class GamePhase(ConfigEnum):
    STRATEGY = auto()
    ACTION = auto()
    STATUS = auto()
    AGENDA = auto()
