from pathlib import Path
from types import MappingProxyType

from app.config.objs.index import index_by_id
from app.config.objs.text_merge import load_and_merge_text_by_id

from .base import PromissoryNoteConfig
from .standard import StandardPromissoryNoteConfig
from .faction import FactionPromissoryNoteConfig

def load_promissory_note_data(root_data_path: Path) -> MappingProxyType[str, PromissoryNoteConfig]:

    rel_path_base = Path("promissory_notes")

    faction_data = load_and_merge_text_by_id(root_data_path, rel_path_base / "faction.yaml")
    data = [FactionPromissoryNoteConfig(**config) for config in faction_data]

    standard_data = load_and_merge_text_by_id(root_data_path, rel_path_base / "standard.yaml")
    data.extend([StandardPromissoryNoteConfig.from_dict(config) for config in standard_data])

    return index_by_id(data)
