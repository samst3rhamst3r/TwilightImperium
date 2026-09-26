from dataclasses import dataclass

from app.config.fromdict import FromDictMixin

from .type import TechType

@dataclass(frozen=True, kw_only=True)
class TechUpgradeReqConfig(FromDictMixin):
    tech_type: TechType
    num: int

    @classmethod
    def _init_from_dict(cls, d: dict) -> None:
        d["tech_type"] = TechType(d["tech_type"])