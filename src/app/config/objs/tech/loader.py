from pathlib import Path
from types import MappingProxyType

from app.config.objs.text_merge import merge_text_by_id, TEXT_CONFIG_OBJ_DATA_PATH
from app.config.objs.index import index_by_id
from app.config.yaml_loader import load_data, load_folder_data

from .ids import TechID
from .tech import AssimilatorTechConfig, StandardTechConfig, TechConfig

_ASSIMILATOR_TECH_IDS = frozenset({TechID.VALEFAR_ASSIMILATOR_X, TechID.VALEFAR_ASSIMILATOR_Y})

def _tech_from_dict(d: dict) -> TechConfig:
    """Dispatch by id (a known discriminator), never by whether tech_type happens to be absent."""
    if d["id"] in _ASSIMILATOR_TECH_IDS:
        return AssimilatorTechConfig(**d)
    return StandardTechConfig.from_dict(d)

def load_tech_data(root_data_path: Path) -> MappingProxyType[str, TechConfig]:
    data = load_folder_data(root_data_path / "techs")
    text_data = load_data(root_data_path / TEXT_CONFIG_OBJ_DATA_PATH / "techs.yaml")
    merged_data = merge_text_by_id(data, text_data)
    
    return index_by_id(_tech_from_dict(tech_config) for tech_config in merged_data)
