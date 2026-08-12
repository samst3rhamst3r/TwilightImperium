"""Tests for app.state.card.action.ActionCardState."""
import pytest

from app.state.card.action import ActionCardState

@pytest.fixture
def action_card_factory():
    def _make(**overrides) -> ActionCardState:
        defaults = {"config_id": "direct_hit", "flavor_text_index": 0}
        return ActionCardState(**(defaults | overrides))
    return _make

def test_action_card_state_has_a_fresh_instance_id_per_instance(action_card_factory) -> None:
    a = action_card_factory()
    b = action_card_factory()
    assert a.instance_id != b.instance_id

def test_action_card_state_save_load_round_trip(action_card_factory, declared_immutable_field_violations) -> None:
    card = action_card_factory(config_id="sabotage", flavor_text_index=2)

    reloaded = ActionCardState.load(card.save())

    assert reloaded.config_id == "sabotage"
    assert reloaded.instance_id == card.instance_id
    assert reloaded.flavor_text_index == 2
    assert not declared_immutable_field_violations(card)
    assert not declared_immutable_field_violations(reloaded)
