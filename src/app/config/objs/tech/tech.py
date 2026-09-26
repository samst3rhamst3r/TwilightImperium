from dataclasses import dataclass

from app.config.objs.named import NamedConfigObj
from app.config.objs.mixins import CanBeExhaustible, CanHaveFactionExclusivity, RequiresFunctionalText

from .type import TechType
from .upgrade_req import TechUpgradeReqConfig

@dataclass(frozen=True, kw_only=True)
class TechConfig(NamedConfigObj, RequiresFunctionalText, CanHaveFactionExclusivity, CanBeExhaustible):
    tech_type: TechType
    prereqs: tuple[TechUpgradeReqConfig, ...] = ()
