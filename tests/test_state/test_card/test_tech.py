"""Tests for app.state.card.tech.TechCardState.

Only ConfigIDStateObj + Exhaustible - tech *ownership* lives many:many on
PlayerState.researched_tech_ids (see specs/STATE_OBJS.md's "Agenda/Tech card
population strategy" open question); this class only tracks the mutable
exhaustion state a subset of technologies can have."""
import pytest

from app.state.card.tech import TechCardState

@pytest.fixture
def tech_card_factory():
    def _make(**overrides) -> TechCardState:
        defaults = {"config_id": "graviton_laser_system"}
        return TechCardState(**(defaults | overrides))
    return _make

def test_tech_card_state_defaults_to_not_exhausted(tech_card_factory) -> None:
    assert tech_card_factory().exhausted is False

def test_tech_card_state_exhaust_and_ready(tech_card_factory) -> None:
    card = tech_card_factory()
    card.exhaust()
    assert card.exhausted is True
    card.ready()
    assert card.exhausted is False

def test_tech_card_state_save_load_round_trip(tech_card_factory, declared_immutable_field_violations) -> None:
    card = tech_card_factory(config_id="graviton_laser_system")
    card.exhaust()

    reloaded = TechCardState.load(card.save())

    assert reloaded.config_id == "graviton_laser_system"
    assert reloaded.exhausted is True
    assert not declared_immutable_field_violations(reloaded)
