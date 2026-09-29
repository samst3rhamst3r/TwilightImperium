from pathlib import Path
from types import MappingProxyType

from app.config.yaml_loader import load_data, CONFIG_OBJ_DATA_PATH
from app.config.objs.index import index_by_id

from .system import SystemConfig

def load_system_data(root_data_path: Path) -> MappingProxyType[str, SystemConfig]:
    data = load_data(root_data_path / CONFIG_OBJ_DATA_PATH / "systems.yaml")
    return index_by_id(SystemConfig.from_dict(system_config) for system_config in data)
