from dataclasses import dataclass

from app.config.unit import UnitLocationType

@dataclass(slots=True, frozen=True)
class UnitLocation:
    loc_type: UnitLocationType
    ref_instance_id: str

    @property
    def is_on_planet(self) -> bool:
        return self.loc_type is UnitLocationType.PLANET

    @property
    def is_in_system(self) -> bool:
        return self.loc_type is UnitLocationType.SYSTEM
    
    @property
    def is_on_ship(self) -> bool:
        return self.loc_type is UnitLocationType.SHIP
