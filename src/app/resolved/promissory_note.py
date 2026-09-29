from dataclasses import dataclass

from app.config.objs.promissory_note import (
    FactionPromissoryNoteConfig,
    PromissoryNoteConfig,
    StandardPromissoryNoteConfig,
)
from app.state.card.promissory_note import PromissoryNoteCardState

from .base import BaseResolvedObj

@dataclass(slots=True, frozen=True)
class ResolvedPromissoryNote(BaseResolvedObj[PromissoryNoteCardState, PromissoryNoteConfig]):

    def __post_init__(self):
        if isinstance(self.config, StandardPromissoryNoteConfig) and not self.state.is_issued_to_player:
            raise ValueError(f"Standard promissory notes must have an issuing player color.\nCONFIG: {self.config}")
        if isinstance(self.config, FactionPromissoryNoteConfig) and self.state.is_issued_to_player:
            raise ValueError(f"Faction promissory notes cannot have an issuing player color.\nCOLOR: {self.state.issuing_player_color}\nCONFIG: {self.config}")

    @property
    def functional_text(self) -> str:
        if isinstance(self.config, StandardPromissoryNoteConfig):
            return f" {self.state.issuing_player_color} ".join(self.config.player_color_functional_text)
        return self.config.functional_text
