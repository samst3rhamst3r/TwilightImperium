"""Mirrors src/app/config/objs/planet/loader.py."""
from types import MappingProxyType

from app.config.objs.planet import PlanetConfig, load_planet_data

def test_loads_a_populated_id_keyed_index(data_dir) -> None:
    index = load_planet_data(data_dir)
    assert isinstance(index, MappingProxyType)
    assert index
    for key, config in index.items():
        assert isinstance(config, PlanetConfig)
        assert key == config.id

def test_flavor_text_is_merged_onto_every_planet(data_dir) -> None:
    for planet in load_planet_data(data_dir).values():
        assert planet.flavor_text, f"{planet.id} has no flavor_text"
