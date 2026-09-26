from dataclasses import dataclass

from app.config.fromdict import FromDictMixin

from .named import NamedConfigObj
from .mixins import RequiresFunctionalText

@dataclass(frozen=True, kw_only=True)
class ActionCardConfig(NamedConfigObj, RequiresFunctionalText, FromDictMixin):
    flavor_text_options: tuple[str, ...]
    num_in_deck: int = 1

    @classmethod
    def _init_from_dict(cls, d: dict) -> None:
        d["flavor_text_options"] = tuple(d["flavor_text_options"])
