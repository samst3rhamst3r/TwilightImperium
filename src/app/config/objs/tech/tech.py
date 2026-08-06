from dataclasses import dataclass

from app.config.shared import NamedConfigObj
from app.config.shared.text_objs import RequiresFunctionalText

from .upgrade_req import TechUpgradeReqConfig
from .type import TechType

@dataclass(frozen=True, kw_only=True, slots=True)
class TechConfig(NamedConfigObj, RequiresFunctionalText):
    tech_type: TechType
    prereqs: tuple[TechUpgradeReqConfig, ...] = ()
    