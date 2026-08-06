from dataclasses import dataclass

from .base import CanHaveFactionExclusivity

@dataclass(slots=True, frozen=True, kw_only=True)
class PromissoryNoteConfig(CanHaveFactionExclusivity):
    pass