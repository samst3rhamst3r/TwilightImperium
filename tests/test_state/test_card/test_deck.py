"""Tests for app.state.card.deck.CardDeckState - the generic deck/discard
container, polymorphic over the small set of card types it actually manages
(ActionCardState, PublicObjectiveCardState, SecretObjectiveCardState - see
_TYPE_REGISTRY; AgendaCardState/TechCardState/PromissoryNoteCardState/
StrategyCardState are deliberately not deck-managed, see game.py)."""
import pytest

from app.state.card.action import ActionCardState
from app.state.card.deck import CardDeckState, EmptyCardDeckError
from app.state.card.objective.public import PublicObjectiveCardState

@pytest.fixture
def action_cards() -> list[ActionCardState]:
    return [
        ActionCardState(config_id="direct_hit", flavor_text_index=0),
        ActionCardState(config_id="sabotage", flavor_text_index=1),
    ]

def test_deck_starts_with_an_empty_discard_pile_by_default(action_cards) -> None:
    deck = CardDeckState(deck=list(action_cards))
    assert deck.discard_pile == []

def test_draw_pops_from_the_deck(action_cards) -> None:
    deck = CardDeckState(deck=list(action_cards))
    drawn = deck.draw()
    assert drawn is action_cards[-1]
    assert drawn not in deck.deck

def test_draw_from_empty_deck_raises() -> None:
    deck = CardDeckState(deck=[])
    with pytest.raises(EmptyCardDeckError):
        deck.draw()

def test_discard_appends_to_discard_pile(action_cards) -> None:
    deck = CardDeckState(deck=[])
    deck.discard(action_cards[0])
    assert deck.discard_pile == [action_cards[0]]

def test_shuffle_discard_pile_back_into_deck_moves_and_clears_discard(action_cards) -> None:
    deck = CardDeckState(deck=[])
    deck.discard(action_cards[0])
    deck.discard(action_cards[1])

    deck.shuffle_discard_pile_back_into_deck()

    assert deck.discard_pile == []
    assert len(deck.deck) == len(action_cards)
    assert all(card in deck.deck for card in action_cards)

def test_shuffle_discard_pile_back_into_deck_is_a_no_op_when_discard_is_empty(action_cards) -> None:
    deck = CardDeckState(deck=list(action_cards))
    deck.shuffle_discard_pile_back_into_deck()
    assert deck.deck == action_cards

def test_card_deck_state_save_load_round_trip_with_action_cards() -> None:
    deck = CardDeckState(
        deck=[
            ActionCardState(config_id="direct_hit", flavor_text_index=0),
            ActionCardState(config_id="sabotage", flavor_text_index=1),
        ],
        discard_pile=[],
    )

    reloaded = CardDeckState.load(deck.save())

    assert [c.config_id for c in reloaded.deck] == ["direct_hit", "sabotage"]
    assert all(isinstance(c, ActionCardState) for c in reloaded.deck)
    assert reloaded.discard_pile == []

def test_card_deck_state_save_load_round_trip_preserves_type_per_card() -> None:
    """The $type-keyed _TYPE_REGISTRY must resolve each card back to its own
    concrete class, not just whatever the deck's declared TCard is."""
    deck = CardDeckState(
        deck=[PublicObjectiveCardState(config_id="mecatol_rex")],
        discard_pile=[ActionCardState(config_id="direct_hit", flavor_text_index=0)],
    )

    reloaded = CardDeckState.load(deck.save())

    assert isinstance(reloaded.deck[0], PublicObjectiveCardState)
    assert isinstance(reloaded.discard_pile[0], ActionCardState)
