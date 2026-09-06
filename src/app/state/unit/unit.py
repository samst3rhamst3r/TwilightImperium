from dataclasses import dataclass

from app.config.objs.unit import UnitLocationType
from app.state.base.mixins import UUIDInstancedStateObj
from app.state.base.ownable import PlayerOwnableMixin, OwnershipError

from .location import UnitLocation

class UnitOwnershipError(OwnershipError):
    """Raised when trying to assign ownership of a unit that is already owned by another player."""
    entity_name: str = "unit"

@dataclass(kw_only=True)
class UnitState(UUIDInstancedStateObj, PlayerOwnableMixin):
    # A deployed unit always occupies exactly one place on the board - there is
    # no "exists but nowhere" state. A unit that has no location has been
    # destroyed and removed from GameState.deployed_units entirely, not left
    # behind with location=None.
    location: UnitLocation
    current_damage: int = 0

    def place_on_ship(self, ship_instance_id: str) -> None:
        self.location = UnitLocation(loc_type=UnitLocationType.SHIP, location_id=ship_instance_id)

    def place_on_planet(self, planet_id: str) -> None:
        self.location = UnitLocation(loc_type=UnitLocationType.PLANET, location_id=planet_id)

    def place_in_system(self, system_id: str) -> None:
        self.location = UnitLocation(loc_type=UnitLocationType.SYSTEM, location_id=system_id)

    def take_hit(self) -> None:
        self.current_damage += 1

    def repair(self) -> None:
        self.current_damage -= 1
        if self.current_damage < 0:
            self.current_damage = 0

    def save(self) -> dict:
        return super().save() | {
            "location": self.location.save(),
            "current_damage": self.current_damage,
        }

    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        self.location = UnitLocation.load(data["location"])
        self.current_damage = data["current_damage"]