from dataclasses import dataclass

from ..shared import CanHaveFactionExclusivity

@dataclass(slots=True, frozen=True, kw_only=True)
class PromissoryNoteConfig(CanHaveFactionExclusivity):
    pass