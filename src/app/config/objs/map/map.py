from dataclasses import dataclass

from app.config.fromdict import FromDictMixin
from app.config.objs.id import IDConfigObj

from app.geometry.coordinate import HexCoordinate

@dataclass(frozen=True)
class MapConfig(IDConfigObj, FromDictMixin):
    tiles: tuple[HexCoordinate, ...]

    @classmethod
    def _init_from_dict(cls, d: dict) -> None:
        d["tiles"] = tuple(HexCoordinate(*coord) for coord in d["tiles"])