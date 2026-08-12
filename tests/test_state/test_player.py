"""Tests for app.state.player.PlayerState."""
import pytest

from app.config.player_color import PlayerColor
from app.state.player import (
    AlreadyHaveSecretObjectiveError,
    AlreadyResearchedTechError,
    AlreadyScoredObjectiveError,
    DoesNotHaveSecretObjectiveError,
    InvalidTokenRedistributionError,
    InvalidTradeGoodsToGiveError,
    NotEnoughCommoditiesError,
    PlayerState,
    TooManyTokensError,
)

@pytest.fixture
def player_factory():
    def _make(**overrides) -> PlayerState:
        defaults = {"id": PlayerColor.RED, "name": "Sam", "faction_config_id": "sol"}
        return PlayerState(**(defaults | overrides))
    return _make

def test_player_state_obj_id_is_the_color(player_factory) -> None:
    assert player_factory().obj_id == PlayerColor.RED

def test_command_token_reinforcement_pool_computed_from_the_three_pools(player_factory) -> None:
    player = player_factory(tactic_pool=3, fleet_pool=3, strategy_pool=2)
    assert player.command_token_reinforcement_pool == 16 - 3 - 3 - 2

def test_construction_raises_when_pools_exceed_max_tokens(player_factory) -> None:
    with pytest.raises(TooManyTokensError):
        player_factory(tactic_pool=10, fleet_pool=10, strategy_pool=10)

def test_score_public_objective(player_factory) -> None:
    player = player_factory()
    player.score_public_objective("card-1")
    assert "card-1" in player.scored_objective_card_ids

def test_score_public_objective_twice_raises(player_factory) -> None:
    player = player_factory()
    player.score_public_objective("card-1")
    with pytest.raises(AlreadyScoredObjectiveError):
        player.score_public_objective("card-1")

def test_bonus_victory_points_score_and_decrement(player_factory) -> None:
    player = player_factory()
    player.score_bonus_victory_points(2)
    assert player.bonus_victory_points == 2
    player.decrement_bonus_victory_points(1)
    assert player.bonus_victory_points == 1

def test_bonus_victory_points_does_not_go_below_zero(player_factory) -> None:
    player = player_factory()
    player.decrement_bonus_victory_points(5)
    assert player.bonus_victory_points == 0

def test_research_tech(player_factory) -> None:
    player = player_factory()
    player.research_tech("tech-1")
    assert "tech-1" in player.researched_tech_ids

def test_research_tech_twice_raises(player_factory) -> None:
    player = player_factory()
    player.research_tech("tech-1")
    with pytest.raises(AlreadyResearchedTechError):
        player.research_tech("tech-1")

def test_commodities_give_and_clear(player_factory) -> None:
    player = player_factory()
    player.set_commodities(3)
    assert player.has_commodities
    given = player.give_commodities(2)
    assert given == 2
    assert player.commodities == 1
    player.clear_commodities()
    assert player.commodities == 0
    assert not player.has_commodities

def test_set_commodities_below_one_raises(player_factory) -> None:
    with pytest.raises(ValueError):
        player_factory().set_commodities(0)

def test_give_more_commodities_than_available_raises(player_factory) -> None:
    player = player_factory()
    player.set_commodities(1)
    with pytest.raises(NotEnoughCommoditiesError):
        player.give_commodities(2)

def test_receive_trade_goods(player_factory) -> None:
    player = player_factory()
    player.receive_trade_goods(3)
    assert player.trade_goods == 3

def test_receive_trade_goods_below_one_raises(player_factory) -> None:
    with pytest.raises(InvalidTradeGoodsToGiveError):
        player_factory().receive_trade_goods(0)

def test_add_and_remove_secret_objective(player_factory) -> None:
    player = player_factory()
    player.add_secret_objective("secret-1")
    assert player.has_secret_objective("secret-1")
    player.remove_secret_objective("secret-1")
    assert not player.has_secret_objective("secret-1")

def test_add_secret_objective_twice_raises(player_factory) -> None:
    player = player_factory()
    player.add_secret_objective("secret-1")
    with pytest.raises(AlreadyHaveSecretObjectiveError):
        player.add_secret_objective("secret-1")

def test_remove_secret_objective_not_held_raises(player_factory) -> None:
    with pytest.raises(DoesNotHaveSecretObjectiveError):
        player_factory().remove_secret_objective("secret-1")

def test_redistribute_command_tokens(player_factory) -> None:
    player = player_factory(tactic_pool=3, fleet_pool=3, strategy_pool=2)
    reinforcement_before = player.command_token_reinforcement_pool

    player.redistribute_command_tokens(tactic_pool=4, fleet_pool=2, strategy_pool=2)

    assert (player.tactic_pool, player.fleet_pool, player.strategy_pool) == (4, 2, 2)
    # Total placed is unchanged (8), so the derived reinforcement pool doesn't move.
    assert player.command_token_reinforcement_pool == reinforcement_before

def test_redistribute_command_tokens_changing_the_total_raises(player_factory) -> None:
    player = player_factory(tactic_pool=3, fleet_pool=3, strategy_pool=2)
    with pytest.raises(InvalidTokenRedistributionError):
        player.redistribute_command_tokens(tactic_pool=4, fleet_pool=4, strategy_pool=4)

def test_player_state_save_load_round_trip(player_factory, declared_immutable_field_violations) -> None:
    player = player_factory(id=PlayerColor.BLUE, name="Sam", faction_config_id="sol")
    player.score_public_objective("card-1")
    player.research_tech("tech-1")
    player.add_secret_objective("secret-1")
    player.set_commodities(2)
    player.receive_trade_goods(1)
    player.score_bonus_victory_points(1)
    player.unit_reinforcement_pool = {}

    reloaded = PlayerState.load(player.save())

    assert reloaded.id is PlayerColor.BLUE
    assert reloaded.name == "Sam"
    assert reloaded.faction_config_id == "sol"
    assert reloaded.scored_objective_card_ids == {"card-1"}
    assert reloaded.researched_tech_ids == {"tech-1"}
    assert reloaded.secret_objective_card_ids_in_hand == {"secret-1"}
    assert reloaded.commodities == 2
    assert reloaded.trade_goods == 1
    assert reloaded.bonus_victory_points == 1
    assert reloaded.command_token_reinforcement_pool == player.command_token_reinforcement_pool
    assert not declared_immutable_field_violations(reloaded)
