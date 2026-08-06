from enum import auto

from app.config.shared.enum import ConfigEnum

class AgendaType(ConfigEnum):
    DIRECTIVE = auto()
    LAW = auto()
