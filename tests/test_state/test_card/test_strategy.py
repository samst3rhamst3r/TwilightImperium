"""Tests for app.state.card.strategy.StrategyCardState."""
import pytest

from app.state.card.strategy import StrategyCardState

@pytest.fixture
def strategy_card_factory():
    def _make(**overrides) -> StrategyCardState:
        defaults = {"config_id": "leadership"}
        return StrategyCardState(**(defaults | overrides))
    return _make

def test_strategy_card_state_defaults_to_not_exhausted(strategy_card_factory) -> None:
    assert strategy_card_factory().exhausted is False

def test_strategy_card_state_exhaust_and_ready(strategy_card_factory) -> None:
    card = strategy_card_factory()
    card.exhaust()
    assert card.exhausted is True
    card.ready()
    assert card.exhausted is False

def test_strategy_card_state_save_load_round_trip(strategy_card_factory, declared_immutable_field_violations) -> None:
    card = strategy_card_factory(config_id="warfare")
    card.exhaust()

    reloaded = StrategyCardState.load(card.save())

    assert reloaded.config_id == "warfare"
    assert reloaded.exhausted is True
    assert not declared_immutable_field_violations(reloaded)
