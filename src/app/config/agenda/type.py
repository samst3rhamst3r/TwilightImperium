from enum import auto

from app.config.enum import ConfigEnum

class AgendaType(ConfigEnum):
    DIRECTIVE = auto()
    LAW = auto()
