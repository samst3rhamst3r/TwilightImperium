
from dataclasses import dataclass, field

from app.config.faction import FactionConfig
from app.config.player import MAX_CONTROL_TOKENS, MAX_COMMAND_TOKENS
from app.config.unit import UnitClass

from .base import BaseStateObj

class AlreadyScoredObjectiveError(Exception):
    pass
class AlreadyResearchedTechError(Exception):
    pass
class NotEnoughCommoditiesError(Exception):
    pass
class InvalidTradeGoodsToGiveError(Exception):
    pass

@dataclass(slots=True, kw_only=True)
class Player(BaseStateObj):
    faction: FactionConfig
    scored_objective_card_ids: set[str] = field(default_factory=set)
    researched_tech_ids: set[str] = field(default_factory=set)
    commodities: int = 0
    trade_goods: int = 0
    victory_pts: int = 0
    
    unit_reinforcement_pool: dict[UnitClass, int] = field(default_factory=dict)
    control_token_pool: int = MAX_CONTROL_TOKENS
    command_token_pool: int = MAX_COMMAND_TOKENS

    def score_objective(self, card_id: str, victory_pts: int) -> None:
        if card_id in self.scored_objective_card_ids:
            raise AlreadyScoredObjectiveError(f"Objective with ID {card_id} has already been scored.")
        self.scored_objective_card_ids.add(card_id)
        self.score_victory_points(victory_pts)

    def score_victory_points(self, pts: int) -> None:
        self.victory_pts += pts

    def decrement_victory_points(self, pts: int) -> None:
        self.victory_pts -= pts
        if self.victory_pts < 0:
            self.victory_pts = 0

    def research_tech(self, tech_id: str) -> None:
        if tech_id in self.researched_tech_ids:
            raise AlreadyResearchedTechError(f"Tech with ID {tech_id} has already been researched.")
        self.researched_tech_ids.add(tech_id)

    def replenish_commodities(self) -> None:
        self.commodities = self.faction.max_commodities

    @property
    def has_commodities(self) -> bool:
        return self.commodities > 0

    def give_commodities(self, amount: int) -> int:
        if amount > self.commodities:
            raise NotEnoughCommoditiesError(f"Only {self.commodities} are available.")
        self.commodities -= amount
        return amount

    def receive_trade_goods(self, amount: int) -> None:
        if amount < 1:
            raise InvalidTradeGoodsToGiveError("Number of trade goods to give must be at least 1.")
        self.trade_goods += amount