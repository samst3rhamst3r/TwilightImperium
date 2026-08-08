from dataclasses import dataclass

from app.config.shared import NamedConfigObj
from app.config.shared.mixins import IsExhaustible, RequiresFlavorText
from app.config.objs.tech import TechType

from .trait import PlanetTrait

@dataclass(slots=True, frozen=True, kw_only=True)
class PlanetConfig(NamedConfigObj, RequiresFlavorText, IsExhaustible):
    system_id: str
    resources: int = 0
    influence: int = 0
    tech_specialty: TechType | None = None
    trait: PlanetTrait | None = None
