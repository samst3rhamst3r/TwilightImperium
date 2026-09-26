"""Tests for app.state.card.promissory_note.PromissoryNoteCardState."""
import pytest

from app.config.player_color import PlayerColor
from app.state.card.promissory_note import PromissoryNoteCardState

@pytest.fixture
def promissory_note_factory():
    def _make(**overrides) -> PromissoryNoteCardState:
        defaults = {"config_id": "trade_agreement"}
        return PromissoryNoteCardState(**(defaults | overrides))
    return _make

def test_promissory_note_defaults_to_unissued(promissory_note_factory) -> None:
    note = promissory_note_factory()
    assert note.issuing_player_color is None
    assert not note.is_issued_to_player

def test_promissory_note_is_issued_to(promissory_note_factory) -> None:
    note = promissory_note_factory(issuing_player_color=PlayerColor.RED)
    assert note.is_issued_to_player
    assert note.is_issued_to(PlayerColor.RED)
    assert not note.is_issued_to(PlayerColor.BLUE)

def test_promissory_note_save_load_round_trip_when_issued(declared_immutable_field_violations, promissory_note_factory) -> None:
    note = promissory_note_factory(issuing_player_color=PlayerColor.RED)

    reloaded = PromissoryNoteCardState.load(note.save())

    assert reloaded.issuing_player_color is PlayerColor.RED
    assert not declared_immutable_field_violations(reloaded)

def test_promissory_note_save_load_round_trip_when_unissued(promissory_note_factory) -> None:
    """Regression: init_from_save used to unconditionally call
    PlayerColor(data["issuing_player_color"]), which crashed on the
    legitimate None case (a note not yet issued to anyone)."""
    note = promissory_note_factory()
    assert note.issuing_player_color is None

    reloaded = PromissoryNoteCardState.load(note.save())

    assert reloaded.issuing_player_color is None
    assert not reloaded.is_issued_to_player
