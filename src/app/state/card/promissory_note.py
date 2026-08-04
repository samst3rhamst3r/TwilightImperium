from dataclasses import dataclass
from typing import Final

from app.config.player_color import PlayerColor
from app.config.base import CanHaveFactionExclusivity
from app.config.text import FunctionalTextConfig

from ..base.state_obj import ConfigBoundStateObj, TextBoundStateObjMixin
from ..base import PlayerOwnable

@dataclass(slots=True, kw_only=True)
class PromissoryNoteCardState(ConfigBoundStateObj[CanHaveFactionExclusivity], TextBoundStateObjMixin[FunctionalTextConfig], PlayerOwnable):
    issuing_player_color: Final[PlayerColor | None] = None

    def __post_init__(self):
        if self.issuing_player_color is None and not self.config.is_faction_exclusive:
            raise ValueError(f"Non-faction exclusive promissory notes must have an issuing player color.\nCONFIG: {self.config}")
        if self.issuing_player_color is not None and self.config.is_faction_exclusive:
            raise ValueError(f"Faction exclusive promissory notes cannot have an issuing player color.\nCOLOR: {self.issuing_player_color}\nCONFIG: {self.config}")

    @property
    def functional_text(self) -> str:
        if self.issuing_player_color is None:
            return self.text_config.functional_text
        else:
            return self.text_config.functional_text.replace("__PLAYER_COLOR__", self.issuing_player_color.value)
