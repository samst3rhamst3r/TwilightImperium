"""Tests for app.state.card.objective.public.PublicObjectiveCardState."""
import pytest

from app.state.card.objective.base import InvalidStateTransition, Revealable
from app.state.card.objective.public import PublicObjectiveCardState

@pytest.fixture
def public_objective_factory():
    def _make(**overrides) -> PublicObjectiveCardState:
        defaults = {"config_id": "mecatol_rex"}
        return PublicObjectiveCardState(**(defaults | overrides))
    return _make

def test_public_objective_explicitly_implements_revealable() -> None:
    """Parity with SecretObjectiveCardState, which already declares this.
    Revealable isn't @runtime_checkable, so this checks explicit inheritance
    via the MRO rather than issubclass() (which Protocol disallows here)."""
    assert Revealable in PublicObjectiveCardState.__mro__

def test_public_objective_starts_unrevealed(public_objective_factory) -> None:
    assert public_objective_factory().is_revealed is False

def test_public_objective_reveal_sets_revealed(public_objective_factory) -> None:
    card = public_objective_factory()
    card.reveal()
    assert card.is_revealed is True

def test_public_objective_reveal_when_already_revealed_raises(public_objective_factory) -> None:
    card = public_objective_factory()
    card.reveal()
    with pytest.raises(InvalidStateTransition):
        card.reveal()

def test_public_objective_save_load_round_trip(public_objective_factory) -> None:
    card = public_objective_factory(config_id="mecatol_rex")
    card.reveal()

    reloaded = PublicObjectiveCardState.load(card.save())

    assert reloaded.config_id == "mecatol_rex"
    assert reloaded.is_revealed is True
