from dataclasses import dataclass

from app.config.fromdict import FromDictMixin

from .base import PromissoryNoteConfig

@dataclass(frozen=True, kw_only=True)
class StandardPromissoryNoteConfig(PromissoryNoteConfig, FromDictMixin):
    player_color_functional_text: tuple[str, ...]

    @classmethod
    def _init_from_dict(cls, data: dict) -> None:
        data["player_color_functional_text"] = tuple(data["player_color_functional_text"])
