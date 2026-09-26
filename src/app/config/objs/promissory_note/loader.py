from .base import PromissoryNoteConfig
from .standard import StandardPromissoryNoteConfig
from .faction import FactionPromissoryNoteConfig

def load_promissory_note_config(data: dict) -> PromissoryNoteConfig:
    if "faction_exclusive_id" in data:
        return FactionPromissoryNoteConfig(**data)
    else:
        return StandardPromissoryNoteConfig(**data)