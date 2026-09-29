from pathlib import Path
from types import MappingProxyType

from app.config.yaml_loader import load_data, CONFIG_OBJ_DATA_PATH
from app.config.objs.index import index_by_id

from .faction import FactionConfig

def load_faction_data(root_data_path: Path) -> MappingProxyType[str, FactionConfig]:
    return index_by_id(FactionConfig.from_dict(config) for config in load_data(root_data_path / CONFIG_OBJ_DATA_PATH / "factions.yaml"))
