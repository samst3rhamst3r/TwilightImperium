from dataclasses import dataclass

from app.config.shared import NamedConfigObj
from app.config.shared.mixins import CanBeExhaustible, CanHaveFactionExclusivity, RequiresFunctionalText

from .type import TechType
from .upgrade_req import TechUpgradeReqConfig

@dataclass(frozen=True, kw_only=True, slots=True)
class TechConfig(NamedConfigObj, RequiresFunctionalText, CanHaveFactionExclusivity, CanBeExhaustible):
    prereqs: tuple[TechUpgradeReqConfig, ...] = ()

@dataclass(frozen=True, kw_only=True, slots=True)
class StandardTechConfig(TechConfig):
    """A real technology - has a fixed tech_type from the moment it's drawn/owned."""
    tech_type: TechType

@dataclass(frozen=True, kw_only=True, slots=True)
class AssimilatorTechConfig(TechConfig):
    """Nekro Virus's Valefar Assimilator X/Y tokens (see TechID). These aren't a
    technology in their own right - they take on whatever tech_type the
    technology they assimilate has, so they carry no static tech_type of
    their own. Pass-through: no fields beyond TechConfig's."""
    pass
