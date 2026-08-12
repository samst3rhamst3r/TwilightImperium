from dataclasses import dataclass
from typing import Final

from app.config.objs.unit import UnitLocationType

from app.state.base import Serializable

@dataclass(kw_only=True)
class UnitLocation(Serializable):
    loc_type: UnitLocationType
    location_id: Final[str]

    @property
    def is_on_planet(self) -> bool:
        return self.loc_type is UnitLocationType.PLANET

    @property
    def is_in_system(self) -> bool:
        return self.loc_type is UnitLocationType.SYSTEM
    
    @property
    def is_on_ship(self) -> bool:
        return self.loc_type is UnitLocationType.SHIP

    def save(self) -> dict:
        return super().save() | {
            "loc_type": self.loc_type.value,
            "location_id": self.location_id,
        }

    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        self.loc_type = UnitLocationType(data["loc_type"])
        self.location_id = data["location_id"]
