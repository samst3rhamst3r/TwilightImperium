"""Mirrors src/app/config/objs/faction/loader.py."""
from types import MappingProxyType

from app.config.objs.faction import FactionConfig, load_faction_data

def test_loads_a_populated_id_keyed_index(data_dir) -> None:
    index = load_faction_data(data_dir)
    assert isinstance(index, MappingProxyType)
    assert index
    for key, config in index.items():
        assert isinstance(config, FactionConfig)
        assert key == config.id

def test_loads_without_a_text_objs_file(data_dir) -> None:
    """factions.yaml has no text_objs counterpart - the loader must read
    objs/ directly rather than requiring a text merge."""
    assert not (data_dir / "text_objs" / "factions.yaml").exists()
    assert load_faction_data(data_dir)

def test_starting_units_are_fully_typed(data_dir) -> None:
    from app.config.objs.faction import FactionStartingUnitConfig
    for faction in load_faction_data(data_dir).values():
        assert faction.starting_units, f"{faction.id} has no starting units"
        assert all(isinstance(u, FactionStartingUnitConfig) for u in faction.starting_units)
