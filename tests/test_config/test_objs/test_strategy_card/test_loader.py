"""Mirrors src/app/config/objs/strategy_card/loader.py."""
from types import MappingProxyType

from app.config.objs.strategy_card import StrategyCardConfig, load_strategy_card_data

def test_loads_a_populated_id_keyed_index(data_dir) -> None:
    index = load_strategy_card_data(data_dir)
    assert isinstance(index, MappingProxyType)
    assert index
    for key, config in index.items():
        assert isinstance(config, StrategyCardConfig)
        assert key == config.id

def test_ability_text_is_merged_onto_every_card(data_dir) -> None:
    """primary/secondary ability text lives only in text_objs/ - regression
    guard for a loader that reads objs/ alone."""
    for card in load_strategy_card_data(data_dir).values():
        assert card.primary_ability_text, f"{card.id} has no primary_ability_text"
        assert card.secondary_ability_text, f"{card.id} has no secondary_ability_text"
