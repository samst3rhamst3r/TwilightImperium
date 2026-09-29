"""Mirrors src/app/config/objs/agenda/agenda.py."""
import pytest

from app.config.objs.agenda import AgendaConfig, AgendaType, AgendaVoteScenarioType
from app.config.objs.planet import PlanetTrait
from app.config.objs.named import NamedConfigObj
from app.config.objs.mixins import RequiresFunctionalText
from app.config.objs.mixins import CanBeExhaustible

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

def test_from_dict_coerces_raw_yaml_strings_to_enums() -> None:
    """Coercion lives in _init_from_dict (the loader boundary), not
    __post_init__ - the constructor only ever receives already-typed values
    (ARCHITECTURE.md section 2). This is what makes the `is`-based
    vote_scenario_type check in __post_init__ reliable."""
    agenda = AgendaConfig.from_dict({
        "id": "x", "name": "X", "functional_text": "...",
        "agenda_type": "law", "vote_scenario_type": "elect_planet", "planet_trait": "industrial",
    })
    assert agenda.agenda_type is AgendaType.LAW
    assert agenda.vote_scenario_type is AgendaVoteScenarioType.ELECT_PLANET
    assert agenda.planet_trait is PlanetTrait.INDUSTRIAL

def test_from_dict_leaves_absent_planet_trait_as_none() -> None:
    agenda = AgendaConfig.from_dict({
        "id": "x", "name": "X", "functional_text": "...",
        "agenda_type": "directive", "vote_scenario_type": "for_against",
    })
    assert agenda.planet_trait is None

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
