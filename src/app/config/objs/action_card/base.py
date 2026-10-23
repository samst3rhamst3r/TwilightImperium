from dataclasses import dataclass

from app.config.shared import NamedConfigObj
from app.config.shared.mixins import RequiresFunctionalText

@dataclass(frozen=True, kw_only=True)
class ActionCardConfig(NamedConfigObj, RequiresFunctionalText):
    flavor_text_options: tuple[str, ...]
    num_in_deck: int = 1

    @classmethod
    def _parse_fields(cls, d: dict) -> None:
        d["flavor_text_options"] = tuple(d["flavor_text_options"])
