from pathlib import Path
from types import MappingProxyType

from config.objs.text_merge import load_data, CONFIG_OBJ_DATA_PATH
from config.objs.index import index_by_id

from .base import StrategyCardConfig

def load_strategy_card_data(root_data_path: Path) -> MappingProxyType[str, StrategyCardConfig]:
    data = load_data(root_data_path / CONFIG_OBJ_DATA_PATH / "strategy_cards.yaml")
    return index_by_id(StrategyCardConfig(**config) for config in data)
