from dataclasses import dataclass
from typing import Optional

from .shared.obj_ import ConfigObj
from ..types.planet_trait import PlanetTrait
from ..types.tech_type import TechType

@dataclass(slots=True, frozen=True, kw_only=True)
class PlanetConfig(ConfigObj):
    name: str
    resources: int = 0
    influence: int = 0
    tech_specialty: Optional[TechType] = None
    trait: Optional[PlanetTrait] = None
