from dataclasses import dataclass

from app.config.base import BaseConfigObj
from app.config.unit import UnitClass

@dataclass(slots=True, frozen=True, kw_only=True)
class FactionStartingUnitConfig(BaseConfigObj):
    unit_class: UnitClass
    num: int
