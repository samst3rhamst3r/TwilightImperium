from collections.abc import Generator
from pathlib import Path

from app.config.shared.loader import load_config_obj_data
from .base import PromissoryNoteConfig

def load_promissory_note_data(root_data_path: Path) -> Generator[PromissoryNoteConfig]:
    for config in load_config_obj_data(root_data_path, "promissory_notes.yaml"):
        yield PromissoryNoteConfig(**config)
