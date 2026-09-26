from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

from app.config.fromdict import FromDictMixin

@dataclass(frozen=True, kw_only=True)
class ParameterizedAbilityInstanceConfig(FromDictMixin):
    ability_id: str
    instance_args: MappingProxyType[str, Any]

    @classmethod
    def _init_from_dict(cls, d: dict) -> None:
        d["instance_args"] = MappingProxyType(d["instance_args"])