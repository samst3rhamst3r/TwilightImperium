from dataclasses import dataclass

from ..base import ConfigObj
from .upgrade_req import TechUpgradeReqConfig
from .type import TechType

@dataclass(frozen=True, kw_only=True, slots=True)
class TechConfig(ConfigObj):
    name: str
    tech_type: TechType
    prereqs: tuple[TechUpgradeReqConfig, ...] = ()
    