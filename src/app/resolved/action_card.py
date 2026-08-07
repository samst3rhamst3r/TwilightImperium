from dataclasses import dataclass

from app.resolved.base import BaseResolvedObj
from app.state.card.action import ActionCardState
from app.config.objs.action_card import ActionCardConfig

from .shared.protocols import ResolvedFlavorTextOptionsMixin, ResolvedFunctionalTextMixin

@dataclass(slots=True, frozen=True)
class ResolvedActionCard(BaseResolvedObj[ActionCardState, ActionCardConfig], ResolvedFunctionalTextMixin, ResolvedFlavorTextOptionsMixin):
    pass