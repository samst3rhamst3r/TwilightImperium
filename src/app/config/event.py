from dataclasses import dataclass

from .shared.obj_ import ConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class EventCardConfig(ConfigObj):
    name: str
    num_in_deck: int = 1