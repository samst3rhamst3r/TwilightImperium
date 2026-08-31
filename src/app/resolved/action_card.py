from dataclasses import dataclass

from app.resolved.base import BaseResolvedObj
from app.state.card.action import ActionCardState
from app.config.objs.action_card import ActionCardConfig

@dataclass(slots=True, frozen=True)
class ResolvedActionCard(BaseResolvedObj[ActionCardState, ActionCardConfig]):

    @property
    def flavor_text(self) -> str:
        return self.config.flavor_text_options[self.state.flavor_text_index]
