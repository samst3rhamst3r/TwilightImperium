from dataclasses import dataclass

from app.config.fromdict import FromDictMixin
from app.config.objs.named import NamedConfigObj
from app.config.objs.mixins import CanBeExhaustible, CanHaveFactionExclusivity, RequiresFunctionalText

from .type import TechType
from .upgrade_req import TechUpgradeReqConfig

@dataclass(frozen=True, kw_only=True)
class TechConfig(NamedConfigObj, RequiresFunctionalText, CanHaveFactionExclusivity, CanBeExhaustible, FromDictMixin):
    tech_type: TechType
    prereqs: tuple[TechUpgradeReqConfig, ...] = ()

    @classmethod
    def _init_from_dict(cls, d: dict) -> None:
        d["tech_type"] = TechType(d["tech_type"])
        d["prereqs"] = tuple(TechUpgradeReqConfig.from_dict(req) for req in d.get("prereqs", ()))
