from dataclasses import dataclass

from app.config.fromdict import FromDictMixin
from app.config.objs.named import NamedConfigObj
from app.config.objs.mixins import CanBeExhaustible, CanHaveFactionExclusivity, RequiresFactionExclusivity, RequiresFunctionalText

from .type import TechType
from .upgrade_req import TechUpgradeReqConfig

@dataclass(frozen=True, kw_only=True)
class TechConfig(NamedConfigObj, RequiresFunctionalText):
    pass

@dataclass(frozen=True, kw_only=True)
class StandardTechConfig(TechConfig, CanHaveFactionExclusivity, CanBeExhaustible, FromDictMixin):
    """A real technology - has a fixed tech_type from the moment it's drawn/owned."""
    prereqs: tuple[TechUpgradeReqConfig, ...] = ()
    tech_type: TechType

    @classmethod
    def _init_from_dict(cls, d: dict) -> None:
        d["prereqs"] = tuple(TechUpgradeReqConfig.from_dict(req) for req in d.get("prereqs", ()))
        d["tech_type"] = TechType(d["tech_type"])

@dataclass(frozen=True, kw_only=True)
class AssimilatorTechConfig(TechConfig, RequiresFactionExclusivity):
    """Nekro Virus's Valefar Assimilator X/Y tokens (see TechID). These aren't a
    technology in their own right - they take on whatever tech_type the
    technology they assimilate has, so they carry no static tech_type of
    their own. Pass-through: no fields beyond TechConfig's."""
    pass
