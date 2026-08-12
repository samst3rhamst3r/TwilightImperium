"""Tests for app.state.card.agenda.AgendaCardState.

Only ConfigIDStateObj + Exhaustible - agendas have no owner (see
specs/STATE_OBJS.md's "Agenda/Tech card population strategy" open question)."""
import pytest

from app.state.card.agenda import AgendaCardState

@pytest.fixture
def agenda_card_factory():
    def _make(**overrides) -> AgendaCardState:
        defaults = {"config_id": "holy_planet_of_ixth"}
        return AgendaCardState(**(defaults | overrides))
    return _make

def test_agenda_card_state_defaults_to_not_exhausted(agenda_card_factory) -> None:
    assert agenda_card_factory().exhausted is False

def test_agenda_card_state_exhaust_and_ready(agenda_card_factory) -> None:
    card = agenda_card_factory()
    card.exhaust()
    assert card.exhausted is True
    card.ready()
    assert card.exhausted is False

def test_agenda_card_state_save_load_round_trip(agenda_card_factory, declared_immutable_field_violations) -> None:
    card = agenda_card_factory(config_id="holy_planet_of_ixth")
    card.exhaust()

    reloaded = AgendaCardState.load(card.save())

    assert reloaded.config_id == "holy_planet_of_ixth"
    assert reloaded.exhausted is True
    assert not declared_immutable_field_violations(reloaded)
