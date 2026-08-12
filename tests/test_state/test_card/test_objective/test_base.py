"""Tests for app.state.card.objective.base - ObjectiveCardState, Revealable,
InvalidStateTransition."""
import pytest

from app.state.card.objective.base import InvalidStateTransition, ObjectiveCardState

def test_invalid_state_transition_is_a_real_exception() -> None:
    """Regression: this class used to not subclass Exception, so raising it
    would crash with TypeError instead of propagating the intended error."""
    assert issubclass(InvalidStateTransition, Exception)
    with pytest.raises(InvalidStateTransition):
        raise InvalidStateTransition("boom")

def test_objective_card_state_save_load_round_trip() -> None:
    card = ObjectiveCardState(config_id="mecatol_rex")
    reloaded = ObjectiveCardState.load(card.save())
    assert reloaded.config_id == "mecatol_rex"
