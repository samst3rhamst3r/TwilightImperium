from dataclasses import dataclass, field
from typing import Optional
from collections.abc import Sequence

from ..types.unit_class import UnitClass
from .shared.obj_ import NamedConfigObj, BaseConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class StartingUnitConfig(BaseConfigObj):
    unit_class: UnitClass
    num: int

@dataclass(slots=True, frozen=True, kw_only=True)
class FactionConfig(NamedConfigObj):
    max_commodities: int
    starting_units: Sequence[StartingUnitConfig]
    starting_tech_ids: Optional[Sequence[str]] = field(default_factory=tuple)
