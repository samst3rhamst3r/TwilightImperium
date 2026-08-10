from dataclasses import dataclass

from app.config.shared import BaseConfigObj

from .type import TechType

@dataclass(slots=True, frozen=True, kw_only=True)
class TechUpgradeReqConfig(BaseConfigObj):
    tech_type: TechType
    num: int

    def __post_init__(self):
        object.__setattr__(self, "tech_type", TechType(self.tech_type))