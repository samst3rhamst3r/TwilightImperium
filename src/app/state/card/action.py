from dataclasses import dataclass
from typing import Self

from app.config.shared import NamedConfigObj

from app.state.base import PlayerOwnable

from .base import CardState

@dataclass(slots=True, kw_only=True)
class ActionCardState(CardState, PlayerOwnable):
    flavor_text_index: int

    def to_save_dict(self) -> dict:
        d  = CardState[NamedConfigObj].to_save_dict(self)
        d |= PlayerOwnable.to_save_dict(self)
        return d | {
            "flavor_text_index": self.flavor_text_index
        }

    @classmethod
    def from_save_dict(cls, config: NamedConfigObj, **kwargs) -> Self:
        return cls(config=config, **kwargs)
    