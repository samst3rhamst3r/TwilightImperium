from dataclasses import dataclass

from app.config.objs.unit import UnitLocationType

from app.state.base import Serializable

@dataclass(slots=True, frozen=True)
class UnitLocation(Serializable):
    loc_type: UnitLocationType
    unit_id: str

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
            "unit_id": self.unit_id,
        }

    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        self.location = UnitLocationType(data["loc_type"])
        self.current_damage = data["current_damage"]
