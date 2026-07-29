from dataclasses import dataclass

from .shared.obj_ import BaseConfigObj
from ..types.tech_type import TechType

@dataclass(slots=True, frozen=True, kw_only=True)
class TechReqConfig(BaseConfigObj):
    tech_type: TechType
    num: int
