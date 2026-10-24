from dataclasses import dataclass

from app.config.shared import BaseConfigObj
from app.config.objs.unit import UnitClass

@dataclass(frozen=True, kw_only=True)
class FactionStartingUnitConfig(BaseConfigObj):
    unit_class: UnitClass
    num: int

    @classmethod
    def _parse_fields(cls, d: dict) -> None:
        d["unit_class"] = UnitClass(d["unit_class"])