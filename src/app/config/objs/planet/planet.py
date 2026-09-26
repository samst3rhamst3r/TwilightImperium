from dataclasses import dataclass

from app.config.fromdict import FromDictMixin
from app.config.objs.named import NamedConfigObj
from app.config.objs.mixins import RequiresFlavorText
from app.config.objs.tech import TechType

from .trait import PlanetTrait

@dataclass(frozen=True, kw_only=True)
class PlanetConfig(NamedConfigObj, RequiresFlavorText, FromDictMixin):
    system_id: str
    resources: int = 0
    influence: int = 0
    tech_specialty: TechType | None = None
    trait: PlanetTrait | None = None

    @classmethod
    def _init_from_dict(cls, d: dict) -> None:
        if "tech_specialty" in d:
            d["tech_specialty"] = TechType(d["tech_specialty"])
        if "trait" in d:
            d["trait"] = PlanetTrait(d["trait"])
