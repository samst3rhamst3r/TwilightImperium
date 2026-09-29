from dataclasses import dataclass

from app.config.fromdict import FromDictMixin
from app.config.objs.unit import UnitClass

@dataclass(frozen=True, kw_only=True)
class FactionStartingUnitConfig(FromDictMixin):
    unit_class: UnitClass
    num: int

    @classmethod
    def _init_from_dict(cls, d: dict) -> None:
        d["unit_class"] = UnitClass(d["unit_class"])
