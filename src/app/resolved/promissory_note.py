from dataclasses import dataclass

from app.config.objs.promissory_note import PromissoryNoteConfig
from app.state.card.promissory_note import PromissoryNoteCardState

from .base import BaseResolvedObj

@dataclass(slots=True, frozen=True)
class ResolvedPromissoryNote(BaseResolvedObj[PromissoryNoteCardState, PromissoryNoteConfig]):

    def __post_init__(self):
        super().__post_init__()

        if self.state.is_issued_to_player and not self.config.is_faction_exclusive:
            raise ValueError(f"Non-faction exclusive promissory notes must have an issuing player color.\nCONFIG: {self.config}")
        if not self.state.is_issued_to_player and self.config.is_faction_exclusive:
            raise ValueError(f"Faction exclusive promissory notes cannot have an issuing player color.\nCOLOR: {self.state.issuing_player_color}\nCONFIG: {self.config}")

    @property
    def functional_text(self) -> str:
        if self.state.is_issued_to_player:
            return self.config.functional_text.replace(self.config.PLAYER_COLOR_REPLACE_STRING, self.state.issuing_player_color)
        else:
            return self.config.functional_text
