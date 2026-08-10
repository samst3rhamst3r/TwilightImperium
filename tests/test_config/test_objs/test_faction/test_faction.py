"""Mirrors src/app/config/objs/faction/faction.py."""
from app.config.objs.faction import FactionConfig
from app.config.shared import NamedConfigObj

def test_faction_config_inherits_named_config_obj() -> None:
    assert issubclass(FactionConfig, NamedConfigObj)

def test_starting_tech_ids_defaults_to_empty() -> None:
    faction = FactionConfig(
        id="x", name="X", max_commodities=3, home_system_id="sys", starting_units=(),
    )
    assert faction.starting_tech_ids == ()

def test_real_faction_data_references_a_real_home_system(ruleset_config) -> None:
    for faction in ruleset_config.factions.values():
        assert faction.home_system_id in ruleset_config.systems
