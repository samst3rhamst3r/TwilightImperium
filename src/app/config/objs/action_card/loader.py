from pathlib import Path
from types import MappingProxyType

from config.objs.text_merge import load_and_merge_text_by_id
from config.objs.index import index_by_id

from .action_card import ActionCardConfig

def load_action_card_data(root_data_path: Path) -> MappingProxyType[str, ActionCardConfig]:
    return index_by_id(ActionCardConfig.from_dict(config) for config in load_and_merge_text_by_id(root_data_path, "action_cards.yaml"))
