from dataclasses import dataclass

from app.config.unit import UnitLocationType

from app.state.base import BaseStateObj

@dataclass(slots=True, frozen=True)
class UnitLocation(BaseStateObj):
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

    def to_save_dict(self) -> dict:
        return {
            "loc_type": self.loc_type.value,
            "unit_id": self.unit_id,
        }

    @classmethod
    def from_save_dict(cls, loc_type: str, **kwargs):
        return cls(
            loc_type=UnitLocationType(loc_type),
            **kwargs,
        )
