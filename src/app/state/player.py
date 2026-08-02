
from dataclasses import dataclass, field
from typing import Final

from app.config.faction import FactionConfig
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
class NotEnoughTokensError(Exception):
    pass
class TooManyTokensError(Exception):
    pass
class AlreadyHaveSecretObjectiveError(Exception):
    pass
class DoesNotHaveSecretObjectiveError(Exception):
    pass
class InvalidTokenRedistributionError(Exception):
    pass

_MAX_CONTROL_TOKENS: Final[int] = 17
_MAX_COMMAND_TOKENS: Final[int] = 16

@dataclass(slots=True, kw_only=True)
class Player(BaseStateObj):
    faction: FactionConfig
    secret_objective_card_ids: set[str] = field(default_factory=set)
    scored_objective_card_ids: set[str] = field(default_factory=set)
    researched_tech_ids: set[str] = field(default_factory=set)
    commodities: int = 0
    trade_goods: int = 0
    victory_pts: int = 0
    tactic_pool: int = 0
    fleet_pool: int = 0
    strategy_pool: int = 0
    
    unit_reinforcement_pool: dict[UnitClass, int] = field(default_factory=dict)
    control_token_reinforcement_pool: int = _MAX_CONTROL_TOKENS
    command_token_reinforcement_pool: int = field(init=False)

    def __post_init__(self):
        total_tokens_to_rmv = self.tactic_pool + self.fleet_pool + self.strategy_pool
        if total_tokens_to_rmv > _MAX_COMMAND_TOKENS:
            raise TooManyTokensError(f"Initialization error. {self.tactic_pool} tactic + {self.fleet_pool} fleet + {self.strategy_pool} command tokens exceeds maximum allowed: {_MAX_COMMAND_TOKENS}.")
        self.command_token_reinforcement_pool = _MAX_COMMAND_TOKENS - total_tokens_to_rmv

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

    def receive_trade_goods(self, amount: int) -> None:
        if amount < 1:
            raise InvalidTradeGoodsToGiveError("Number of trade goods to give must be at least 1.")
        self.trade_goods += amount

    def give_commodities(self, amount: int) -> int:
        if amount > self.commodities:
            raise NotEnoughCommoditiesError(f"Only {self.commodities} are available.")
        self.commodities -= amount
        return amount

    def receive_control_tokens(self, amount: int) -> None:
        if self.control_token_pool + amount > _MAX_CONTROL_TOKENS:
            raise TooManyTokensError(f"Cannot receive {amount} control tokens; already have {self.control_token_pool}. Maximum allowed is {_MAX_CONTROL_TOKENS}.")
        self.control_token_pool += amount

    def remove_from_control_token_pool(self, amount: int) -> None:
        if amount > self.control_token_pool:
            raise NotEnoughTokensError(f"Only {self.control_token_pool} control tokens are available. Cannot give {amount}.")
        self.control_token_pool -= amount

    def receive_command_tokens(self, amount: int) -> None:
        if self.command_token_pool + amount > _MAX_COMMAND_TOKENS:
            raise TooManyTokensError(f"Cannot receive {amount} command tokens; already have {self.command_token_pool}. Maximum allowed is {_MAX_COMMAND_TOKENS}.")
        self.command_token_pool += amount

    def remove_from_command_token_pool(self, amount: int) -> None:
        if amount > self.command_token_pool:
            raise NotEnoughTokensError(f"Only {self.command_token_pool} command tokens are available. Cannot give {amount}.")
        self.command_token_pool -= amount

    def add_secret_objective(self, card_id: str) -> None:
        if card_id in self.secret_objective_card_ids:
            raise AlreadyHaveSecretObjectiveError(f"Player already has the secret objective with ID {card_id}.")
        self.secret_objective_card_ids.add(card_id)

    def remove_secret_objective(self, card_id: str) -> str:
        if card_id not in self.secret_objective_card_ids:
            raise DoesNotHaveSecretObjectiveError(f"Player does not have the secret objective with ID {card_id}.")
        return self.secret_objective_card_ids.pop(card_id)

    def has_secret_objective(self, card_id: str) -> bool:
        return card_id in self.secret_objective_card_ids

    def redistribute_command_tokens(self, tactic_pool: int, fleet_pool: int, strategy_pool: int) -> None:
        existing = self.tactic_pool + self.fleet_pool + self.strategy_pool
        requested = tactic_pool + fleet_pool + strategy_pool
        if requested != existing:
            raise InvalidTokenRedistributionError(f"The sum of the token pools must equal the sum of existing tactic, fleet, and strategy pools. Existing: {existing}, Requested: {requested}")
        self.tactic_pool = tactic_pool
        self.fleet_pool = fleet_pool
        self.strategy_pool = strategy_pool
