from enum import auto

from app.config.enum import ConfigEnum

class PlanetTrait(ConfigEnum):
    CULTURAL = auto()
    HAZARDOUS = auto()
    INDUSTRIAL = auto()
