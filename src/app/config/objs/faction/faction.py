from dataclasses import dataclass

from app.config.shared import NamedConfigObj

from .starting_unit import FactionStartingUnitConfig

@dataclass(frozen=True, kw_only=True)
class FactionConfig(NamedConfigObj):
    max_commodities: int
    home_system_id: str
    starting_units: tuple[FactionStartingUnitConfig, ...]
    starting_tech_ids: tuple[str, ...] = ()
    off_board_home_system_id: str | None = None # Unique to Ghosts of Creuss
