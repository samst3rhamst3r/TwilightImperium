from dataclasses import dataclass

from app.config.objs.strategy_card import StrategyCardConfig
from app.state.card import StrategyCardState

from .base import BaseResolvedObj
from .shared.protocols import ExhaustibleMixin, PlayerOwnableMixin

@dataclass(slots=True, frozen=True)
class ResolvedStrategyCard(BaseResolvedObj[StrategyCardState, StrategyCardConfig], ExhaustibleMixin, PlayerOwnableMixin):

    # Forwarded to PrimarySecondaryAbilityTextConfig, but didn't create Mixin Protocol like other classes because it's a one-off for this class

    @property
    def primary_ability_text(self) -> str:
        return self.config.primary_ability_text

    @property
    def secondary_ability_text(self) -> str:
        return self.config.secondary_ability_text