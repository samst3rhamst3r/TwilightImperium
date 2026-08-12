from dataclasses import dataclass

from app.config.objs.unit import UnitLocationType
from app.state.base.mixins import UUIDInstancedStateObj

from .location import UnitLocation

@dataclass(kw_only=True)
class UnitState(UUIDInstancedStateObj):
    # A deployed unit always occupies exactly one place on the board - there is
    # no "exists but nowhere" state. A unit that has no location has been
    # destroyed and removed from GameState.deployed_units entirely, not left
    # behind with location=None.
    location: UnitLocation
    current_damage: int = 0

    # def _validate_location(self):
    #     valid_locs = get_valid_locations_for(self.config)
    #     if self.location.loc_type not in valid_locs:
    #         config_cls = self.config.unit_class
    #         valid_locs = get_valid_locations_for(self.config)
    #         if self.location.loc_type not in valid_locs:
    #             raise ValueError(f"Invalid location types for unit of class {config_cls}: {self.location.loc_type.name}\nValid location types include: {', '.join(loc.name for loc in valid_locs)}")

    def place_on_ship(self, ship_instance_id: str) -> None:
        self.location = UnitLocation(loc_type=UnitLocationType.SHIP, location_id=ship_instance_id)

    def place_on_planet(self, planet_id: str) -> None:
        self.location = UnitLocation(loc_type=UnitLocationType.PLANET, location_id=planet_id)

    def place_in_system(self, system_id: str) -> None:
        self.location = UnitLocation(loc_type=UnitLocationType.SYSTEM, location_id=system_id)

    # def move_to_system(self, system_id: str) -> None:
    #     if self.can_move:
    #         self.place_in_system(system_id)
    #     else:
    #         raise ValueError("Unit cannot move")
    
    def take_hit(self) -> None:
        self.current_damage += 1

    def repair(self) -> None:
        self.current_damage -= 1
        if self.current_damage < 0:
            self.current_damage = 0

    # @property
    # def is_about_to_be_destroyed(self) -> bool:
    #     return self.current_damage == self._sustainable_damage - 1
    
    # @property
    # def is_destroyed(self) -> bool:
    #     return self.current_damage == self._sustainable_damage

    # @property
    # def can_move(self) -> bool:
    #     return self.config.move is not None and self.config.move > 0

    # def _does_parameterized_ability_exist(self, ability_id: str) -> bool:
    #     return any(x.ability_id == ability_id for x in self.config.parameterized_abilities)

    # @property
    # def can_use_anti_fighter_barrage(self) -> bool:
    #     return self._does_parameterized_ability_exist(AbilityID.ANTI_FIGHTER_BARRAGE)

    # @property
    # def can_use_space_cannon(self) -> bool:
    #     return self._does_parameterized_ability_exist(AbilityID.SPACE_CANNON)

    # @property
    # def can_use_bombardment(self) -> bool:
    #     return self._does_parameterized_ability_exist(AbilityID.BOMBARDMENT)

    # def _does_standard_ability_exist(self, ability_id: str) -> bool:
    #     return ability_id in self.config.ability_ids

    # @property
    # def can_sustain_damage(self) -> bool:
    #     return self._does_standard_ability_exist(AbilityID.SUSTAIN_DAMAGE)

    def save(self) -> dict:
        return super().save() | {
            "location": self.location.save(),
            "current_damage": self.current_damage,
        }

    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        self.location = UnitLocation.load(data["location"])
        self.current_damage = data["current_damage"]