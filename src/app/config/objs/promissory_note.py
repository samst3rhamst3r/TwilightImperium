from dataclasses import dataclass

from app.config.shared.text_objs import RequiresFunctionalText

from ..shared import CanHaveFactionExclusivity

@dataclass(slots=True, frozen=True, kw_only=True)
class PromissoryNoteConfig(CanHaveFactionExclusivity, RequiresFunctionalText):
    pass