from dataclasses import dataclass
from typing import ClassVar, Final

from app.config.shared import NamedConfigObj, RequiresFunctionalText, CanHaveFactionExclusivity

@dataclass(frozen=True, kw_only=True)
class PromissoryNoteConfig(NamedConfigObj, CanHaveFactionExclusivity, RequiresFunctionalText):

    PLAYER_COLOR_REPLACE_STRING: ClassVar[Final[str]] = "__PLAYER_COLOR__"

    def __post_init__(self):
        if self.faction_exclusive_id is not None and self.PLAYER_COLOR_REPLACE_STRING in self.functional_text:
            raise ValueError("Promissory note with faction exclusivity cannot contain player color placeholder")
