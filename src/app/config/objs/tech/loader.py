from pathlib import Path
from types import MappingProxyType

from config.objs.text_merge import load_and_merge_text_by_id
from config.objs.index import index_by_id

from .tech import TechConfig

def load_tech_data(root_data_path: Path) -> MappingProxyType[str, TechConfig]:
    merged_data = load_and_merge_text_by_id(root_data_path, Path("techs.yaml"))
    return index_by_id(TechConfig.from_dict(tech_config) for tech_config in merged_data)
