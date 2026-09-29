from dataclasses import dataclass

from app.config.fromdict import FromDictMixin
from app.config.objs.named import NamedConfigObj
from app.config.objs.mixins import CanBeExhaustible, CanHaveFactionExclusivity, RequiresFunctionalText

from .type import TechType
from .upgrade_req import TechUpgradeReqConfig

@dataclass(frozen=True, kw_only=True)
class TechConfig(NamedConfigObj, RequiresFunctionalText, CanHaveFactionExclusivity, CanBeExhaustible, FromDictMixin):
    prereqs: tuple[TechUpgradeReqConfig, ...] = ()
    # no tech_type field here - not universal (see AssimilatorTechConfig)

    @classmethod
    def _init_from_dict(cls, d: dict) -> None:
        d["prereqs"] = tuple(TechUpgradeReqConfig.from_dict(req) for req in d.get("prereqs", ()))

@dataclass(frozen=True, kw_only=True)
class StandardTechConfig(TechConfig):
    """A real technology - has a fixed tech_type from the moment it's drawn/owned."""
    tech_type: TechType

    @classmethod
    def _init_from_dict(cls, d: dict) -> None:
        super()._init_from_dict(d)
        d["tech_type"] = TechType(d["tech_type"])

@dataclass(frozen=True, kw_only=True)
class AssimilatorTechConfig(TechConfig):
    """Nekro Virus's Valefar Assimilator X/Y tokens (see TechID). These aren't a
    technology in their own right - they take on whatever tech_type the
    technology they assimilate has, so they carry no static tech_type of
    their own. Pass-through: no fields beyond TechConfig's."""
    pass
