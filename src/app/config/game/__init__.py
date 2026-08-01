from dataclasses import dataclass

from app.config.base import NamedConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class GameConfig(NamedConfigObj):
    players: int
    map_type: str