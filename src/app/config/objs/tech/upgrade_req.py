from dataclasses import dataclass

from app.config.shared import BaseConfigObj

from .type import TechType

@dataclass(frozen=True, kw_only=True)
class TechUpgradeReqConfig(BaseConfigObj):
    tech_type: TechType
    num: int

    @classmethod
    def _parse_fields(cls, d: dict) -> None:
        d["tech_type"] = TechType(d["tech_type"])