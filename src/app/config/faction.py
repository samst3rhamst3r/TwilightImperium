from dataclasses import dataclass, field
from typing import Optional
from collections.abc import Sequence

from app.config.unit import UnitClass
from app.config.shared import NamedConfigObj, BaseConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class FactionStartingUnitConfig(BaseConfigObj):
    unit_class: UnitClass
    num: int

@dataclass(slots=True, frozen=True, kw_only=True)
class FactionConfig(NamedConfigObj):
    max_commodities: int
    home_system_id: str
    starting_units: Sequence[FactionStartingUnitConfig]
    starting_tech_ids: Optional[Sequence[str]] = field(default_factory=tuple)
    off_board_home_system_id: Optional[str] = None # Unique to Ghosts of Creuss
