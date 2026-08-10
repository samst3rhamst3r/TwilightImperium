from dataclasses import dataclass

from app.config.shared import BaseConfigObj
from app.config.objs.unit import UnitClass

@dataclass(frozen=True, kw_only=True)
class FactionStartingUnitConfig(BaseConfigObj):
    unit_class: UnitClass
    num: int

    def __post_init__(self):
        object.__setattr__(self, "unit_class", UnitClass(self.unit_class))