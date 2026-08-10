"""Mirrors src/app/config/objs/agenda/agenda.py."""
import pytest

from app.config.objs.agenda import AgendaConfig, AgendaType, AgendaVoteScenarioType
from app.config.objs.planet import PlanetTrait
from app.config.shared import NamedConfigObj, RequiresFunctionalText
from app.config.shared.mixins import CanBeExhaustible

def test_agenda_config_composes_the_expected_mixins() -> None:
    assert issubclass(AgendaConfig, NamedConfigObj)
    assert issubclass(AgendaConfig, RequiresFunctionalText)
    assert issubclass(AgendaConfig, CanBeExhaustible)

def _make(**overrides):
    defaults = dict(
        id="x", name="X", functional_text="...",
        agenda_type=AgendaType.LAW, vote_scenario_type=AgendaVoteScenarioType.FOR_AGAINST,
    )
    return AgendaConfig(**(defaults | overrides))

@pytest.mark.parametrize("agenda_type", [AgendaType.LAW, "law"], ids=["enum", "str"])
def test_post_init_coerces_agenda_type_from_either_the_enum_or_its_raw_string(agenda_type) -> None:
    """__post_init__ explicitly coerces via object.__setattr__ (required
    since the dataclass is frozen) - this is what makes the `is`-based
    vote_scenario_type check below actually reliable regardless of whether
    the caller passed a real enum member or the raw YAML string."""
    agenda = _make(agenda_type=agenda_type)
    assert agenda.agenda_type is AgendaType.LAW

def test_planet_trait_is_rejected_outside_elect_planet_scenario() -> None:
    with pytest.raises(ValueError):
        _make(vote_scenario_type=AgendaVoteScenarioType.FOR_AGAINST, planet_trait=PlanetTrait.INDUSTRIAL)

def test_planet_trait_is_accepted_for_elect_planet_scenario() -> None:
    agenda = _make(vote_scenario_type=AgendaVoteScenarioType.ELECT_PLANET, planet_trait=PlanetTrait.INDUSTRIAL)
    assert agenda.planet_trait is PlanetTrait.INDUSTRIAL

def test_real_agenda_data_loads_and_coerces_types(ruleset_config) -> None:
    for agenda in ruleset_config.agendas.values():
        assert isinstance(agenda.agenda_type, AgendaType)
        assert isinstance(agenda.vote_scenario_type, AgendaVoteScenarioType)
