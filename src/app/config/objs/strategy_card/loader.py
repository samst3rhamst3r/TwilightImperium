from pathlib import Path
from types import MappingProxyType

from app.config.objs.text_merge import load_and_merge_text_by_id
from app.config.objs.index import index_by_id

from .base import StrategyCardConfig

def load_strategy_card_data(root_data_path: Path) -> MappingProxyType[str, StrategyCardConfig]:
    return index_by_id(StrategyCardConfig(**config) for config in load_and_merge_text_by_id(root_data_path, "strategy_cards.yaml"))
