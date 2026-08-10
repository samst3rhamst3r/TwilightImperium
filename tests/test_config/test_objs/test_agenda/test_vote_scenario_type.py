"""Mirrors src/app/config/objs/agenda/vote_scenario_type.py."""
from app.config.objs.agenda import AgendaVoteScenarioType
from app.config.shared.enum import ConfigEnum

def test_agenda_vote_scenario_type_is_a_configenum() -> None:
    assert issubclass(AgendaVoteScenarioType, ConfigEnum)

def test_agenda_vote_scenario_type_has_the_expected_members() -> None:
    assert {member.value for member in AgendaVoteScenarioType} == {
        "for_against", "elect_player", "elect_planet", "elect_law", "elect_scored_secret_objective",
    }
