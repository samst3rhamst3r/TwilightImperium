from pathlib import Path
from types import MappingProxyType

from config.objs.text_merge import load_and_merge_text_by_id
from config.objs.index import index_by_id

from .faction import FactionConfig

def load_faction_data(root_data_path: Path) -> MappingProxyType[str, FactionConfig]:
    return index_by_id(FactionConfig.from_dict(config) for config in load_and_merge_text_by_id(root_data_path, "factions.yaml"))
