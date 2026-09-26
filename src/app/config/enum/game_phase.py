from enum import auto

from app.config.enum.base import ConfigEnum

class GamePhase(ConfigEnum):
    STRATEGY = auto()
    ACTION = auto()
    STATUS = auto()
    AGENDA = auto()
