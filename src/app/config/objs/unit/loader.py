from pathlib import Path
from types import MappingProxyType

from app.config.objs.text_merge import load_and_merge_text_by_id
from app.config.objs.index import index_by_id

from .unit import UnitConfig

def load_unit_data(root_data_path: Path) -> MappingProxyType[str, UnitConfig]:
    merged_data = load_and_merge_text_by_id(root_data_path, Path("units.yaml"), text_required=False)
    return index_by_id(UnitConfig.from_dict(unit_config) for unit_config in merged_data)
