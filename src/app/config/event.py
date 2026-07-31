from dataclasses import dataclass

from app.config.shared import NamedConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class EventCardConfig(NamedConfigObj):
    pass