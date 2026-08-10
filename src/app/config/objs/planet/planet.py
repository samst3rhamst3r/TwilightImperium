from dataclasses import dataclass

from app.config.shared import NamedConfigObj
from app.config.shared.mixins import RequiresFlavorText
from app.config.objs.tech import TechType

from .trait import PlanetTrait

@dataclass(frozen=True, kw_only=True)
class PlanetConfig(NamedConfigObj, RequiresFlavorText):
    system_id: str
    resources: int = 0
    influence: int = 0
    tech_specialty: TechType | None = None
    trait: PlanetTrait | None = None
