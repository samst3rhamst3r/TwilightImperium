from dataclasses import dataclass

from .base import BaseStateObj

@dataclass(slots=True, kw_only=True, frozen=True)
class MapState(BaseStateObj):
    map_shape_id: str

    def to_save_dict(self) -> dict:
        return {"map_shape_id": self.map_shape_id}
