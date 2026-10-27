from dataclasses import dataclass
from typing import Protocol

from app.state.objs import ConfigIDStateObj

@dataclass(kw_only=True)
class ObjectiveCardState(ConfigIDStateObj):
    pass

class Revealable(Protocol):
    @property
    def is_revealed(self) -> bool: ...
    def reveal(self) -> None: ...

class InvalidStateTransition(Exception):
    pass