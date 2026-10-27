from dataclasses import dataclass

from app.config.objs.planet import PlanetConfig
from app.state.objs.planet import PlanetState 

from .base import BaseResolvedObj
from .exhaust import IsExhaustibleProtocol

@dataclass(slots=True, frozen=True)
class ResolvedPlanet(BaseResolvedObj[PlanetState, PlanetConfig], IsExhaustibleProtocol):
    pass