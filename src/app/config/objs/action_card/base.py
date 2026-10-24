from dataclasses import dataclass

from app.config.shared import NamedConfigObj
from app.config.shared.mixins import RequiresFunctionalText

@dataclass(frozen=True, kw_only=True)
class ActionCardConfig(NamedConfigObj, RequiresFunctionalText):
    flavor_text_options: tuple[str, ...]

    @property
    def num_in_deck(self) -> int:
        return len(self.flavor_text_options)

    @classmethod
    def _parse_fields(cls, d: dict) -> None:
        d["flavor_text_options"] = tuple(d["flavor_text_options"])
