from collections.abc import Generator
from pathlib import Path

from app.config.shared.loader import load_text_data_into_config_by_id
from .base import PromissoryNoteConfig

def load_promissory_note_data(root_data_path: Path) -> Generator[PromissoryNoteConfig]:
    for config in load_text_data_into_config_by_id(root_data_path, "promissory_notes.yaml"):
        yield PromissoryNoteConfig(**config)
