from dataclasses import dataclass

from app.config.shared import BaseConfigObj

from .type import TechType

@dataclass(slots=True, frozen=True, kw_only=True)
class TechUpgradeReqConfig(BaseConfigObj):
    tech_type: TechType
    num: int
