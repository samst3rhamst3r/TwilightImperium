from enum import auto

from app.config.enum.base import ConfigEnum

class AgendaType(ConfigEnum):
    DIRECTIVE = auto()
    LAW = auto()
