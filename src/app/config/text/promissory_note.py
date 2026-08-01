from dataclasses import dataclass

from .text import BaseTextConfig

@dataclass(slots=True, frozen=True, kw_only=True)
class PromissoryNoteTextConfig(BaseTextConfig):
    pass