from dataclasses import dataclass

from app.config.base import NamedConfigObj
from app.config.text import EventTextConfig

from app.state.base import PlayerOwnable

from .base import CardState

class ActionCardOutofBoundsError(IndexError): pass

@dataclass(slots=True, kw_only=True)
class ActionCardState(CardState[NamedConfigObj, EventTextConfig], PlayerOwnable):
    flavor_text_index: int

    def __post_init__(self):
        if self.flavor_text_index < 0 or self.flavor_text_index >= len(self.text_config.flavor_text_options):
            raise ActionCardOutofBoundsError(f"flavor_text_index is out of bounds for Action Card ID {self.config.id}. Must be between 0 and {len(self.text_config.flavor_text_options) - 1}, inclusive.")
        
    @property
    def flavor_text(self) -> str:
        return self.text_config.flavor_text_options[self.flavor_text_index]