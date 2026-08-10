"""Mirrors src/app/config/objs/strategy_card.py."""
from app.config.objs.strategy_card import StrategyCardConfig
from app.config.shared import NamedConfigObj

def test_strategy_card_config_inherits_named_config_obj() -> None:
    assert issubclass(StrategyCardConfig, NamedConfigObj)

def test_real_strategy_card_data_has_eight_unique_initiative_values(ruleset_config) -> None:
    initiatives = [card.initiative for card in ruleset_config.strategy_cards.values()]
    assert len(ruleset_config.strategy_cards) == 8
    assert len(set(initiatives)) == 8
