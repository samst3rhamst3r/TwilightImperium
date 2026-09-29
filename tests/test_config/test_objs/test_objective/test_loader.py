"""Mirrors src/app/config/objs/objective/loader.py."""
from types import MappingProxyType

from app.config.objs.objective import ObjectiveConfig, load_objective_data

def test_loads_a_populated_id_keyed_index(data_dir) -> None:
    index = load_objective_data(data_dir)
    assert isinstance(index, MappingProxyType)
    assert index
    for key, config in index.items():
        assert isinstance(config, ObjectiveConfig)
        assert key == config.id

def test_text_is_merged_onto_every_objective(data_dir) -> None:
    for objective in load_objective_data(data_dir).values():
        assert objective.functional_text, f"{objective.id} has no functional_text"
