from dataclasses import dataclass

from app.config.objs.planet import PlanetConfig
from app.state.planet import PlanetState 

from .base import BaseResolvedObj

@dataclass(slots=True, kw_only=True)
class ResolvedPlanet(BaseResolvedObj[PlanetState, PlanetConfig]):
    pass