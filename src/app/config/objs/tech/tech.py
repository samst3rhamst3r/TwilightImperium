from dataclasses import dataclass

from app.config.shared import NamedConfigObj
from app.config.shared.mixins import RequiresFunctionalText

from .type import TechType
from .upgrade_req import TechUpgradeReqConfig

@dataclass(frozen=True, kw_only=True, slots=True)
class TechConfig(NamedConfigObj, RequiresFunctionalText):
    tech_type: TechType
    prereqs: tuple[TechUpgradeReqConfig, ...] = ()
    