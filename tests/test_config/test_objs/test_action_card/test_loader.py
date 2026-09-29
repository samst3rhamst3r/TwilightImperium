"""Mirrors src/app/config/objs/action_card/loader.py."""
from types import MappingProxyType

from app.config.objs.action_card import ActionCardConfig, load_action_card_data

def test_loads_a_populated_id_keyed_index(data_dir) -> None:
    index = load_action_card_data(data_dir)
    assert isinstance(index, MappingProxyType)
    assert index
    for key, config in index.items():
        assert isinstance(config, ActionCardConfig)
        assert key == config.id

def test_text_is_merged_onto_every_card(data_dir) -> None:
    for card in load_action_card_data(data_dir).values():
        assert card.functional_text, f"{card.id} has no functional_text"
