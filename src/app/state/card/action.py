from dataclasses import dataclass
from typing import Self

from app.config.objs.action_card import ActionCardConfig
from app.config.shared import NamedConfigObj

from app.state.base import PlayerOwnable

from .base import CardState

class ActionCardOutofBoundsError(IndexError): pass

@dataclass(slots=True, kw_only=True)
class ActionCardState(CardState[ActionCardConfig], PlayerOwnable):
    flavor_text_index: int

    def __post_init__(self):
        if self.flavor_text_index < 0 or self.flavor_text_index >= len(self.text_config.flavor_text_options):
            raise ActionCardOutofBoundsError(f"flavor_text_index is out of bounds for Action Card ID {self.config.id}. Must be between 0 and {len(self.text_config.flavor_text_options) - 1}, inclusive.")

    def to_save_dict(self) -> dict:
        d  = CardState[NamedConfigObj].to_save_dict(self)
        d |= PlayerOwnable.to_save_dict(self)
        return d | {
            "flavor_text_index": self.flavor_text_index
        }

    @classmethod
    def from_save_dict(cls, config: NamedConfigObj, **kwargs) -> Self:
        return cls(config=config, **kwargs)
    