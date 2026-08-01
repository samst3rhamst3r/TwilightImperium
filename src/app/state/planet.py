from dataclasses import dataclass

from app.config.planet import PlanetConfig
from .base import BaseStateObj, Exhaustable

@dataclass(slots=True, kw_only=True)
class PlanetState(BaseStateObj[PlanetConfig], Exhaustable):
    pass