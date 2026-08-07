from dataclasses import dataclass

from app.state.base.protocols import Loadable

from .base import CardState

@dataclass(slots=True, kw_only=True)
class ActionCardState(CardState, Loadable):
    flavor_text_index: int

    def to_save_dict(self) -> dict:
        d  = super().to_save_dict(self)
        return d | {
            "flavor_text_index": self.flavor_text_index
        }
