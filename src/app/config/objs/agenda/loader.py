from collections.abc import Generator
from pathlib import Path

from app.config.shared.loader import load_text_data_into_config_by_id
from .base import AgendaConfig

def load_agenda_data(root_data_path: Path) -> Generator[AgendaConfig]:
    for config in load_text_data_into_config_by_id(root_data_path, "agendas.yaml"):
        yield AgendaConfig(**config)
