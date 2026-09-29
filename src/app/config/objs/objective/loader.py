from pathlib import Path
from types import MappingProxyType

from app.config.objs.text_merge import load_and_merge_text_by_id
from app.config.objs.index import index_by_id

from .objective import ObjectiveConfig

def load_objective_data(root_data_path: Path) -> MappingProxyType[str, ObjectiveConfig]:
    return index_by_id(ObjectiveConfig.from_dict(config) for config in load_and_merge_text_by_id(root_data_path, "objectives.yaml"))
