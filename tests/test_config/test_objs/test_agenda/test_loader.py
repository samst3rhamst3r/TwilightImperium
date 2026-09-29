"""Mirrors src/app/config/objs/agenda/loader.py."""
from types import MappingProxyType

from app.config.objs.agenda import AgendaConfig, load_agenda_data

def test_loads_a_populated_id_keyed_index(data_dir) -> None:
    index = load_agenda_data(data_dir)
    assert isinstance(index, MappingProxyType)
    assert index
    for key, config in index.items():
        assert isinstance(config, AgendaConfig)
        assert key == config.id

def test_text_is_merged_onto_every_agenda(data_dir) -> None:
    for agenda in load_agenda_data(data_dir).values():
        assert agenda.functional_text, f"{agenda.id} has no functional_text"
