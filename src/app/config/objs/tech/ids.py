from enum import auto

from app.config.shared.enum import ConfigEnum

class TechID(ConfigEnum):
    """Tech IDs can be enumerated here if there are tech-specific
    configurations required that don't belong in YAML config files
    """
    VALEFAR_ASSIMILATOR_X = auto()
    VALEFAR_ASSIMILATOR_Y = auto()
