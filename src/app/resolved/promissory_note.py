from dataclasses import dataclass
from typing import Final

from app.config.objs.promissory_note import (
    FactionPromissoryNoteConfig,
    PromissoryNoteConfig,
    StandardPromissoryNoteConfig,
)
from app.config.player_color import PlayerColor
from app.state.card.promissory_note import PromissoryNoteCardState

from .base import BaseResolvedObj

@dataclass(slots=True, frozen=True)
class ResolvedPromissoryNote[TConfig: PromissoryNoteConfig](BaseResolvedObj[PromissoryNoteCardState, TConfig]):

    @property
    def functional_text(self) -> str:
        pass

@dataclass(slots=True, frozen=True)
class ResolvedFactionPromissoryNote(ResolvedPromissoryNote[FactionPromissoryNoteConfig]):

    @property
    def functional_text(self) -> str:
        return self.config.functional_text

@dataclass(slots=True, frozen=True)
class ResolvedStandardPromissoryNote(ResolvedPromissoryNote[StandardPromissoryNoteConfig]):
    issuer_color: Final[PlayerColor]

    @property
    def functional_text(self) -> str:
        return f" {self.issuer_color} ".join(self.config.player_color_functional_text)
