from dataclasses import dataclass

from app.config.objs.promissory_note import PromissoryNoteConfig
from app.config.player_color import PlayerColor
from app.state.card.promissory_note import PromissoryNoteCardState

from .base import BaseResolvedObj
from .shared.protocols import CanHaveFactionExclusivityMixin, ResolvedFunctionalTextMixin

@dataclass(slots=True, frozen=True)
class ResolvedPromissoryNote(BaseResolvedObj[PromissoryNoteCardState, PromissoryNoteConfig], CanHaveFactionExclusivityMixin, ResolvedFunctionalTextMixin):

    def __post_init__(self):
        super().__post_init__()

        if self.is_issued_to_player and not self.is_faction_exclusive:
            raise ValueError(f"Non-faction exclusive promissory notes must have an issuing player color.\nCONFIG: {self.config}")
        if not self.is_issued_to_player and self.is_faction_exclusive:
            raise ValueError(f"Faction exclusive promissory notes cannot have an issuing player color.\nCOLOR: {self.issuing_player_color}\nCONFIG: {self.config}")

    @property
    def issuing_player_color(self) -> PlayerColor | None:
        return self.state.issuing_player_color

    @property
    def is_issued_to_player(self) -> bool:
        return self.state.is_issued_to_player

    def is_issued_to(self, player_color: PlayerColor) -> bool:
        return self.state.is_issued_to(player_color)

    @property
    def functional_text(self) -> str:
        if self.is_issued_to_player:
            return self.config.functional_text.replace(self.config.PLAYER_COLOR_REPLACE_STRING, self.issuing_player_color)
        else:
            return super().functional_text
