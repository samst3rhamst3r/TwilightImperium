"""Mirrors src/app/config/objs/planet/planet.py."""
from app.config.objs.planet import PlanetConfig
from app.config.shared import NamedConfigObj
from app.config.shared.mixins import RequiresFlavorText

def test_planet_config_composes_the_expected_mixins() -> None:
    assert issubclass(PlanetConfig, NamedConfigObj)
    assert issubclass(PlanetConfig, RequiresFlavorText)

def test_resources_and_influence_default_to_zero() -> None:
    planet = PlanetConfig(id="x", name="X", flavor_text="...", system_id="sys")
    assert planet.resources == 0
    assert planet.influence == 0

def test_real_planet_data_references_a_real_system(ruleset_config) -> None:
    for planet in ruleset_config.planets.values():
        assert planet.system_id in ruleset_config.systems
