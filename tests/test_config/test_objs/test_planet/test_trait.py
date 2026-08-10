"""Mirrors src/app/config/objs/planet/trait.py."""
from app.config.objs.planet import PlanetTrait
from app.config.shared.enum import ConfigEnum

def test_planet_trait_is_a_configenum() -> None:
    assert issubclass(PlanetTrait, ConfigEnum)

def test_planet_trait_has_the_expected_members() -> None:
    assert {member.value for member in PlanetTrait} == {"cultural", "hazardous", "industrial"}
