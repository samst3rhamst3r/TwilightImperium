
from dataclasses import dataclass, field
from typing import Final, Self

from app.config.objs.unit import UnitClass
from app.config.player_color import PlayerColor
from app.state.base.mixins import IDedStateObj

class AlreadyScoredObjectiveError(Exception):
    pass
class AlreadyResearchedTechError(Exception):
    pass
class NotEnoughCommoditiesError(Exception):
    pass
class InvalidTradeGoodsToGiveError(Exception):
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

@dataclass(kw_only=True)
class PlayerState(IDedStateObj):
    # PlayerColor is a SerializableEnum (StrEnum), so it already satisfies
    # IDedStateObj.obj_id's `-> str` contract directly - no separate `.value`
    # unwrap needed, matching how ConfigIDStateObj.config_id/UUIDInstancedStateObj.instance_id
    # each provide obj_id from their own identifying field.
    id: Final[PlayerColor]
    name: Final[str]
    faction_config_id: Final[str]
    secret_objective_card_ids_in_hand: set[str] = field(default_factory=set)
    scored_objective_card_ids: set[str] = field(default_factory=set)
    researched_tech_ids: set[str] = field(default_factory=set)
    commodities: int = 0
    trade_goods: int = 0
    bonus_victory_points: int = 0
    tactic_pool: int = _NEW_GAME_DEFAULT_TACTIC_POOL_SIZE
    fleet_pool: int = _NEW_GAME_DEFAULT_FLEET_POOL_SIZE
    strategy_pool: int = _NEW_GAME_DEFAULT_STRATEGY_POOL_SIZE
    
    unit_reinforcement_pool: dict[UnitClass, int] = field(default_factory=dict)

    @property
    def obj_id(self) -> str:
        return self.id

    @property
    def command_token_reinforcement_pool(self) -> int:
        """Derived, not stored - always the printed max minus whatever's
        currently placed across the three command-sheet pools, so it can
        never drift out of sync with them (nothing to save/restore either)."""
        return _MAX_COMMAND_TOKENS - self.tactic_pool - self.fleet_pool - self.strategy_pool

    def save(self) -> dict:
        return super().save() | {
            "id": self.id,
            "name": self.name,
            "faction_config_id": self.faction_config_id,
            "secret_objective_card_ids_in_hand": list(self.secret_objective_card_ids_in_hand),
            "scored_objective_card_ids": list(self.scored_objective_card_ids),
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

        self.id = PlayerColor(data["id"])
        self.name = data["name"]
        self.faction_config_id = data["faction_config_id"]
        self.secret_objective_card_ids_in_hand = set(data["secret_objective_card_ids_in_hand"])
        self.scored_objective_card_ids = set(data["scored_objective_card_ids"])
        self.researched_tech_ids = set(data["researched_tech_ids"])
        self.commodities = data["commodities"]
        self.trade_goods = data["trade_goods"]
        self.bonus_victory_points = data["bonus_victory_points"]
        self.tactic_pool = data["tactic_pool"]
        self.fleet_pool = data["fleet_pool"]
        self.strategy_pool = data["strategy_pool"]
        self.unit_reinforcement_pool = {UnitClass(k): v for k, v in data["unit_reinforcement_pool"].items()}

    def __post_init__(self):
        self.id = PlayerColor(self.id)
        total_tokens_placed = self.tactic_pool + self.fleet_pool + self.strategy_pool
        if total_tokens_placed > _MAX_COMMAND_TOKENS:
            raise TooManyTokensError(f"Initialization error. {self.tactic_pool} tactic + {self.fleet_pool} fleet + {self.strategy_pool} command tokens exceeds maximum allowed: {_MAX_COMMAND_TOKENS}.")
        self.secret_objective_card_ids_in_hand = set(self.secret_objective_card_ids_in_hand)
        self.scored_objective_card_ids = set(self.scored_objective_card_ids)
        self.researched_tech_ids = set(self.researched_tech_ids)

    def score_public_objective(self, card_id: str) -> None:
        if card_id in self.scored_objective_card_ids:
            raise AlreadyScoredObjectiveError(f"Public objective with ID {card_id} has already been scored.")
        self.scored_objective_card_ids.add(card_id)

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

    def add_secret_objective(self, card_id: str) -> None:
        if card_id in self.secret_objective_card_ids_in_hand:
            raise AlreadyHaveSecretObjectiveError(f"Player already has the secret objective with ID {card_id}.")
        self.secret_objective_card_ids_in_hand.add(card_id)

    def remove_secret_objective(self, card_id: str) -> None:
        if not self.has_secret_objective(card_id):
            raise DoesNotHaveSecretObjectiveError(f"Player does not have the secret objective with ID {card_id}.")
        self.secret_objective_card_ids_in_hand.remove(card_id)

    def has_secret_objective(self, card_id: str) -> bool:
        return card_id in self.secret_objective_card_ids_in_hand

    def redistribute_command_tokens(self, tactic_pool: int, fleet_pool: int, strategy_pool: int) -> None:
        existing = self.tactic_pool + self.fleet_pool + self.strategy_pool
        requested = tactic_pool + fleet_pool + strategy_pool
        if requested != existing:
            raise InvalidTokenRedistributionError(f"The sum of the token pools must equal the sum of existing tactic, fleet, and strategy pools. Existing: {existing}, Requested: {requested}")
        self.tactic_pool = tactic_pool
        self.fleet_pool = fleet_pool
        self.strategy_pool = strategy_pool
