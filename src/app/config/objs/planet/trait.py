from enum import auto

from app.config.enum.base import ConfigEnum

class PlanetTrait(ConfigEnum):
    CULTURAL = auto()
    HAZARDOUS = auto()
    INDUSTRIAL = auto()
