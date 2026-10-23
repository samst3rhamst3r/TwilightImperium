from collections.abc import Generator
from pathlib import Path

from app.config.shared.loader import load_text_data_into_config_by_id
from .base import StrategyCardConfig

def load_strategy_card_data(root_data_path: Path) -> Generator[StrategyCardConfig]:
    for config in load_text_data_into_config_by_id(root_data_path, "strategy_cards.yaml"):
        yield StrategyCardConfig(**config)
