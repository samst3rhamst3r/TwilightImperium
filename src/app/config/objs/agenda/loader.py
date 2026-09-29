from pathlib import Path
from types import MappingProxyType

from app.config.objs.text_merge import load_and_merge_text_by_id
from app.config.objs.index import index_by_id

from .agenda import AgendaConfig

def load_agenda_data(root_data_path: Path) -> MappingProxyType[str, AgendaConfig]:
    return index_by_id(AgendaConfig.from_dict(config) for config in load_and_merge_text_by_id(root_data_path, "agendas.yaml"))
