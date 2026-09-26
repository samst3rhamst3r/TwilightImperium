from dataclasses import dataclass

from app.config.fromdict import FromDictMixin
from app.config.objs.named import NamedConfigObj

from .starting_unit import FactionStartingUnitConfig

@dataclass(frozen=True, kw_only=True)
class FactionConfig(NamedConfigObj, FromDictMixin):
    max_commodities: int
    home_system_id: str
    starting_units: tuple[FactionStartingUnitConfig, ...]
    starting_tech_ids: tuple[str, ...] = ()
    off_board_home_system_id: str | None = None # Unique to Ghosts of Creuss

    @classmethod
    def _init_from_dict(cls, d: dict) -> None:
        d["starting_units"] = tuple(FactionStartingUnitConfig.from_dict(unit) for unit in d["starting_units"])
        d["starting_tech_ids"] = tuple(d.get("starting_tech_ids", ()))