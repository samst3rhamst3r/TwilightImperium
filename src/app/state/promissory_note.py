from dataclasses import dataclass
from typing import Final

from app.config.player_color import PlayerColor
from app.config.promissory_note import PromissoryNoteConfig
from app.state.base import BaseStateObj

@dataclass(slots=True, kw_only=True)
class PromissoryNoteState(BaseStateObj[PromissoryNoteConfig]):

    @property
    def functional_text(self) -> str:
        return self.config.functional_text

@dataclass(slots=True, kw_only=True)
class StandardPromissoryNoteState(PromissoryNoteState):
    issuing_player_color: Final[PlayerColor]

    @property
    def functional_text(self) -> str:
        return self.config.functional_text
