from dataclasses import dataclass

from app.config.shared import NamedConfigObj, RequiresFunctionalText, CanHaveFactionExclusivity

@dataclass(slots=True, frozen=True, kw_only=True)
class PromissoryNoteConfig(NamedConfigObj, CanHaveFactionExclusivity, RequiresFunctionalText):

    def __post_init__(self):
        if self.faction_exclusive_id is not None and "__PLAYER_COLOR__" in self.functional_text:
            raise ValueError("Promissory note with faction exclusivity cannot contain player color placeholder")