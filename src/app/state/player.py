
from dataclasses import dataclass, field
from typing import Final

from app.config.objs.unit import UnitClass
from app.state.base.mixins import UUIDInstancedMixin

from .base.state_obj import StateObj

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

_MAX_COMMAND_TOKENS: Final[int] = 16
_NEW_GAME_DEFAULT_TACTIC_POOL_SIZE: Final[int] = 3
_NEW_GAME_DEFAULT_FLEET_POOL_SIZE: Final[int] = 3
_NEW_GAME_DEFAULT_STRATEGY_POOL_SIZE: Final[int] = 2

@dataclass(slots=True, kw_only=True)
class PlayerState(StateObj, UUIDInstancedMixin):
    name: Final[str]
    faction_id: Final[str]
    secret_objective_card_ids: set[str] = field(default_factory=set)
    scored_public_objective_card_ids: set[str] = field(default_factory=set)
    researched_tech_ids: set[str] = field(default_factory=set)
    commodities: int = 0
    trade_goods: int = 0
    bonus_victory_points: int = 0
    tactic_pool: int = _NEW_GAME_DEFAULT_TACTIC_POOL_SIZE
    fleet_pool: int = _NEW_GAME_DEFAULT_FLEET_POOL_SIZE
    strategy_pool: int = _NEW_GAME_DEFAULT_STRATEGY_POOL_SIZE
    
    unit_reinforcement_pool: dict[UnitClass, int] = field(default_factory=dict)

    # Calculated at initialization based upon size of tactic/fleet/strategy pools
    command_token_reinforcement_pool: int = field(init=False)

    def to_save_dict(self) -> dict:
        return super().to_save_dict() | {
            "name": self.name,
            "faction_id": self.faction_id,
            "secret_objective_card_ids": list(self.secret_objective_card_ids),
            "scored_public_objective_card_ids": list(self.scored_public_objective_card_ids),
            "researched_tech_ids": list(self.researched_tech_ids),
            "commodities": self.commodities,
            "trade_goods": self.trade_goods,
            "bonus_victory_points": self.bonus_victory_points,
            "tactic_pool": self.tactic_pool,
            "fleet_pool": self.fleet_pool,
            "strategy_pool": self.strategy_pool,
            "unit_reinforcement_pool": self.unit_reinforcement_pool,
        }

    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)

        self.name = data["name"]
        self.faction_id = data["faction_id"]
        self.secret_objective_card_ids = set(data["secret_objective_card_ids"])
        self.scored_public_objective_card_ids = set(data["scored_public_objective_card_ids"])
        self.researched_tech_ids = set(data["researched_tech_ids"])
        self.commodities = data["commodities"]
        self.trade_goods = data["trade_goods"]
        self.bonus_victory_points = data["bonus_victory_points"]
        self.tactic_pool = data["tactic_pool"]
        self.fleet_pool = data["fleet_pool"]
        self.strategy_pool = data["strategy_pool"]
        self.unit_reinforcement_pool = {UnitClass(k): v for k, v in data["unit_reinforcement_pool"].items()}
    
    def __post_init__(self):
        super().__post_init__()

        total_tokens_to_rmv = self.tactic_pool + self.fleet_pool + self.strategy_pool
        if total_tokens_to_rmv > _MAX_COMMAND_TOKENS:
            raise TooManyTokensError(f"Initialization error. {self.tactic_pool} tactic + {self.fleet_pool} fleet + {self.strategy_pool} command tokens exceeds maximum allowed: {_MAX_COMMAND_TOKENS}.")
        self.command_token_reinforcement_pool = _MAX_COMMAND_TOKENS - total_tokens_to_rmv
        self.secret_objective_card_ids = set(self.secret_objective_card_ids)
        self.scored_public_objective_card_ids = set(self.scored_public_objective_card_ids)
        self.researched_tech_ids = set(self.researched_tech_ids)

    def score_public_objective(self, card_id: str) -> None:
        if card_id in self.scored_public_objective_card_ids:
            raise AlreadyScoredObjectiveError(f"Public objective with ID {card_id} has already been scored.")
        self.scored_public_objective_card_ids.add(card_id)

    def score_bonus_victory_points(self, pts: int) -> None:
        self.bonus_victory_points += pts

    def decrement_bonus_victory_points(self, pts: int) -> None:
        self.bonus_victory_points -= pts
        if self.bonus_victory_points < 0:
            self.bonus_victory_points = 0

    def research_tech(self, tech_id: str) -> None:
        if tech_id in self.researched_tech_ids:
            raise AlreadyResearchedTechError(f"Tech with ID {tech_id} has already been researched.")
        self.researched_tech_ids.add(tech_id)

    @property
    def has_commodities(self) -> bool:
        return self.commodities > 0

    def clear_commodities(self) -> None:
        self.commodities = 0

    def set_commodities(self, amount: int) -> None:
        if amount < 1:
            raise ValueError("Amount to set commodities must be at least 1.")
        self.commodities = amount

    def give_commodities(self, amount: int) -> int:
        if amount > self.commodities:
            raise NotEnoughCommoditiesError(f"Only {self.commodities} are available.")
        self.commodities -= amount
        return amount

    def receive_trade_goods(self, amount: int) -> None:
        if amount < 1:
            raise InvalidTradeGoodsToGiveError("Number of trade goods to give must be at least 1.")
        self.trade_goods += amount

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

    def remove_secret_objective(self, card_id: str) -> None:
        if not self.has_secret_objective(card_id):
            raise DoesNotHaveSecretObjectiveError(f"Player does not have the secret objective with ID {card_id}.")
        self.secret_objective_card_ids.remove(card_id)

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
