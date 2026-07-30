import enum

class GamePhase(enum.StrEnum):
    STRATEGY = enum.auto()
    ACTION = enum.auto()
    STATUS = enum.auto()
    AGENDA = enum.auto()
