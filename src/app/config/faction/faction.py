from dataclasses import dataclass, field
from typing import Optional
from collections.abc import Sequence

from app.config.base import NamedConfigObj

from .starting_unit import FactionStartingUnitConfig

@dataclass(slots=True, frozen=True, kw_only=True)
class FactionConfig(NamedConfigObj):
    max_commodities: int
    home_system_id: str
    starting_units: Sequence[FactionStartingUnitConfig]
    starting_tech_ids: Optional[Sequence[str]] = field(default_factory=tuple)
    off_board_home_system_id: Optional[str] = None # Unique to Ghosts of Creuss
