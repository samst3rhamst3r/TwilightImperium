"""Mirrors src/app/config/objs/tech/loader.py."""
from types import MappingProxyType

from app.config.objs.tech import TechConfig, load_tech_data

def test_loads_a_populated_id_keyed_index(data_dir) -> None:
    index = load_tech_data(data_dir)
    assert isinstance(index, MappingProxyType)
    assert index
    for key, config in index.items():
        assert isinstance(config, TechConfig)
        assert key == config.id

def test_assimilator_ids_load_as_assimilator_techs(data_dir) -> None:
    from app.config.objs.tech import AssimilatorTechConfig, TechID
    techs = load_tech_data(data_dir)
    assert isinstance(techs[TechID.VALEFAR_ASSIMILATOR_X], AssimilatorTechConfig)
    assert isinstance(techs[TechID.VALEFAR_ASSIMILATOR_Y], AssimilatorTechConfig)

def test_every_other_tech_loads_as_a_standard_tech(data_dir) -> None:
    from app.config.objs.tech import StandardTechConfig, TechID
    others = [
        tech for id_, tech in load_tech_data(data_dir).items()
        if id_ not in (TechID.VALEFAR_ASSIMILATOR_X, TechID.VALEFAR_ASSIMILATOR_Y)
    ]
    assert others, "expected at least one real (non-assimilator) tech in the data"
    assert all(isinstance(tech, StandardTechConfig) for tech in others)
