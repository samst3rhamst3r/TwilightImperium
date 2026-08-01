from dataclasses import dataclass
from typing import Final, Optional

from app.config.player_color import PlayerColor
from app.config.base import CanHaveFactionExclusivity
from app.config.text import FunctionalTextConfig

from .base import BaseStateObj

@dataclass(slots=True, kw_only=True)
class PromissoryNoteState(BaseStateObj[CanHaveFactionExclusivity, FunctionalTextConfig]):
    issuing_player_color: Final[Optional[PlayerColor]] = None
    current_holder_id: Optional[str] = None

    def __post_init__(self):
        if self.issuing_player_color is None and not self.config.is_faction_exclusive:
            raise ValueError(f"Non-faction exclusive promissory notes must have an issuing player color.\nCONFIG: {self.config}")
        if self.issuing_player_color is not None and self.config.is_faction_exclusive:
            raise ValueError(f"Faction exclusive promissory notes cannot have an issuing player color.\nCOLOR: {self.issuing_player_color}\nCONFIG: {self.config}")