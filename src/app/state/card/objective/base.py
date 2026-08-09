from dataclasses import dataclass
from typing import Protocol

from app.state.base.mixins import ConfigIDInstancedStateObj

@dataclass(slots=True, kw_only=True)
class ObjectiveCardState(ConfigIDInstancedStateObj):
    pass

class Revealable(Protocol):
    @property
    def is_revealed(self) -> bool: ...
    def reveal(self) -> None: ...

class InvalidStateTransition:
    pass