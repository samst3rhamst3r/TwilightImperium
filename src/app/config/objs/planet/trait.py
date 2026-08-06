from enum import auto

from app.config.shared.enum import ConfigEnum

class PlanetTrait(ConfigEnum):
    CULTURAL = auto()
    HAZARDOUS = auto()
    INDUSTRIAL = auto()
