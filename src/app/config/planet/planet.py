from dataclasses import dataclass
from typing import Optional

from app.config.base import ConfigObj
from app.config.tech import TechType

from .trait import PlanetTrait

@dataclass(slots=True, frozen=True, kw_only=True)
class PlanetConfig(ConfigObj):
    name: str
    system_id: str
    resources: int = 0
    influence: int = 0
    tech_specialty: Optional[TechType] = None
    trait: Optional[PlanetTrait] = None
