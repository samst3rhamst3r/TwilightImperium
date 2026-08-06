from dataclasses import dataclass
from typing import Final, Self

from app.config.player_color import PlayerColor
from app.config.base import CanHaveFactionExclusivity
from app.config.text import FunctionalTextConfig

from app.state.base import ConfigBoundStateObj, TextBoundStateObjMixin, PlayerOwnable

@dataclass(slots=True, kw_only=True)
class PromissoryNoteCardState(ConfigBoundStateObj[CanHaveFactionExclusivity], TextBoundStateObjMixin[FunctionalTextConfig], PlayerOwnable):
    issuing_player_color: Final[PlayerColor | None] = None

    def __post_init__(self):
        if self.issuing_player_color is None and not self.config.is_faction_exclusive:
            raise ValueError(f"Non-faction exclusive promissory notes must have an issuing player color.\nCONFIG: {self.config}")
        if self.issuing_player_color is not None and self.config.is_faction_exclusive:
            raise ValueError(f"Faction exclusive promissory notes cannot have an issuing player color.\nCOLOR: {self.issuing_player_color}\nCONFIG: {self.config}")

    def to_save_dict(self):
        d  = ConfigBoundStateObj[CanHaveFactionExclusivity].to_save_dict(self)
        d |= TextBoundStateObjMixin[FunctionalTextConfig].to_save_dict(self)
        d |= PlayerOwnable.to_save_dict(self)
        return d | {
            "issuing_player_color": self.issuing_player_color
        }

    @classmethod
    def from_save_dict(cls, config: CanHaveFactionExclusivity, text_config: FunctionalTextConfig, issuing_player_color: str | None, **kwargs) -> Self:
        if issuing_player_color is not None:
            issuing_player_color = PlayerColor(issuing_player_color)
        return cls(config=config, text_config=text_config, issuing_player_color=issuing_player_color, **kwargs)
    
    @property
    def functional_text(self) -> str:
        if self.issuing_player_color is None:
            return self.text_config.functional_text
        else:
            return self.text_config.functional_text.replace("__PLAYER_COLOR__", self.issuing_player_color.value)
