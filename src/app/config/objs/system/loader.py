from pathlib import Path
from types import MappingProxyType

from config.objs.text_merge import load_and_merge_text_by_id
from config.objs.index import index_by_id

from .system import SystemConfig

def load_system_data(root_data_path: Path) -> MappingProxyType[str, SystemConfig]:
    merged_data = load_and_merge_text_by_id(root_data_path, Path("systems.yaml"))
    return index_by_id(SystemConfig.from_dict(system_config) for system_config in merged_data)
