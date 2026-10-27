from enum import auto

from app.config.shared.enum import ConfigEnum

class FactionID(ConfigEnum):
    """Factions that have unique configurations that need to be
    referenced throughout the codebase.
    """
    NAALU_COLLECTIVE = auto()
    NEKRO_VIRUS = auto()
    GHOSTS_OF_CREUSS = auto()
