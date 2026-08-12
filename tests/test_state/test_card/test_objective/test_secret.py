"""Tests for app.state.card.objective.secret - SecretObjectiveCardState /
SecretObjectiveZone.

NOTE: whether owner_player_id should be retained through the SCORED zone
transition (vs. released, as release_owner_and_score currently does) is an
open question - see specs/STATE_OBJS.md "Secret objective scored-ownership".
These tests cover the *current* behavior, not a resolution of that question.
"""
import pytest

from app.state.card.objective.base import InvalidStateTransition, Revealable
from app.state.card.objective.secret import SecretObjectiveCardState, SecretObjectiveZone

@pytest.fixture
def secret_objective_factory():
    def _make(**overrides) -> SecretObjectiveCardState:
        defaults = {"config_id": "destroy_their_greatest_ship"}
        return SecretObjectiveCardState(**(defaults | overrides))
    return _make

def test_secret_objective_explicitly_implements_revealable() -> None:
    """Revealable isn't @runtime_checkable, so this checks explicit
    inheritance via the MRO rather than issubclass()."""
    assert Revealable in SecretObjectiveCardState.__mro__

def test_secret_objective_starts_in_deck(secret_objective_factory) -> None:
    card = secret_objective_factory()
    assert card.zone is SecretObjectiveZone.IN_DECK
    assert card.can_be_drawn
    assert not card.is_scored
    assert not card.is_revealed

def test_give_to_player_moves_to_hand_and_assigns_owner(secret_objective_factory) -> None:
    card = secret_objective_factory()
    card.give_to_player("red")
    assert card.zone is SecretObjectiveZone.IN_HAND
    assert card.ownable.is_owned_by_player("red")
    assert card.can_be_scored
    assert card.can_be_discarded

def test_give_to_player_when_not_in_deck_raises(secret_objective_factory) -> None:
    card = secret_objective_factory()
    card.give_to_player("red")
    with pytest.raises(InvalidStateTransition):
        card.give_to_player("blue")

def test_release_owner_and_score_moves_to_scored_and_releases_owner(secret_objective_factory) -> None:
    card = secret_objective_factory()
    card.give_to_player("red")

    released = card.release_owner_and_score()

    assert released == "red"
    assert card.zone is SecretObjectiveZone.SCORED
    assert card.is_scored
    assert not card.ownable.is_owned
    assert card.can_be_revealed

def test_release_owner_and_discard_moves_to_deck_and_releases_owner(secret_objective_factory) -> None:
    card = secret_objective_factory()
    card.give_to_player("red")

    released = card.release_owner_and_discard()

    assert released == "red"
    assert card.zone is SecretObjectiveZone.IN_DECK
    assert not card.ownable.is_owned

def test_release_owner_and_discard_when_not_in_hand_raises(secret_objective_factory) -> None:
    card = secret_objective_factory()
    with pytest.raises(InvalidStateTransition):
        card.release_owner_and_discard()

def test_reveal_requires_scored_zone(secret_objective_factory) -> None:
    card = secret_objective_factory()
    with pytest.raises(InvalidStateTransition):
        card.reveal()

    card.give_to_player("red")
    with pytest.raises(InvalidStateTransition):
        card.reveal()

    card.release_owner_and_score()
    card.reveal()
    assert card.is_revealed
    assert card.zone is SecretObjectiveZone.REVEALED

def test_secret_objective_save_load_round_trip(secret_objective_factory, declared_immutable_field_violations) -> None:
    card = secret_objective_factory(config_id="destroy_their_greatest_ship")
    card.give_to_player("red")

    reloaded = SecretObjectiveCardState.load(card.save())

    assert reloaded.config_id == "destroy_their_greatest_ship"
    assert reloaded.zone is SecretObjectiveZone.IN_HAND
    assert reloaded.ownable.is_owned_by_player("red")
    assert not declared_immutable_field_violations(reloaded)
