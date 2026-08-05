from dataclasses import dataclass, field

from app.config.unit import UnitConfig, UnitLocationType, get_valid_locations_for
from app.config.text import FunctionalTextConfig
from app.config.ability import AbilityID
from app.state.base import ConfigBoundStateObj, TextBoundStateObjMixin, PlayerOwnable

from .location import UnitLocation

@dataclass(slots=True, kw_only=True)
class UnitState(ConfigBoundStateObj[UnitConfig], TextBoundStateObjMixin[FunctionalTextConfig], PlayerOwnable):
    location: UnitLocation | None = None
    current_damage: int = 0
    _sustainable_damage: int = field(init=False)

    def __post_init__(self):

        if self.can_sustain_damage:
            self._sustainable_damage = 2
        else:
            self._sustainable_damage = 1

    def _validate_location(self):
        valid_locs = get_valid_locations_for(self.config)
        if self.location.loc_type not in valid_locs:
            config_cls = self.config.unit_class
            valid_locs = get_valid_locations_for(self.config)
            if self.location.loc_type not in valid_locs:
                raise ValueError(f"Invalid location types for unit of class {config_cls}: {self.location.loc_type.name}\nValid location types include: {', '.join(loc.name for loc in valid_locs)}")

    def place_on_ship(self, ship_instance_id: str) -> None:
        self.location = UnitLocation(UnitLocationType.SHIP, ship_instance_id)
        self._validate_location()

    def place_on_planet(self, planet_id: str) -> None:
        self.location = UnitLocation(UnitLocationType.PLANET, planet_id)
        self._validate_location()

    def place_in_system(self, system_id: str) -> None:
        self.location = UnitLocation(UnitLocationType.SYSTEM, system_id)
        self._validate_location()

    def move_to_system(self, system_id: str) -> None:
        if self.can_move:
            self.place_in_system(system_id)
        else:
            raise ValueError("Unit cannot move")
    
    def take_hit(self) -> None:
        self.current_damage += 1

    def repair(self) -> None:
        self.current_damage -= 1
        if self.current_damage < 0:
            self.current_damage = 0

    @property
    def is_about_to_be_destroyed(self) -> bool:
        return self.current_damage == self._sustainable_damage - 1
    
    @property
    def is_destroyed(self) -> bool:
        return self.current_damage == self._sustainable_damage

    @property
    def can_move(self) -> bool:
        return self.config.move is not None and self.config.move > 0

    def _does_parameterized_ability_exist(self, ability_id: str) -> bool:
        return any(x.ability_id == ability_id for x in self.config.parameterized_abilities)

    @property
    def can_use_anti_fighter_barrage(self) -> bool:
        return self._does_parameterized_ability_exist(AbilityID.ANTI_FIGHTER_BARRAGE)

    @property
    def can_use_space_cannon(self) -> bool:
        return self._does_parameterized_ability_exist(AbilityID.SPACE_CANNON)

    @property
    def can_use_bombardment(self) -> bool:
        return self._does_parameterized_ability_exist(AbilityID.BOMBARDMENT)

    def _does_standard_ability_exist(self, ability_id: str) -> bool:
        return ability_id in self.config.ability_ids

    @property
    def can_sustain_damage(self) -> bool:
        return self._does_standard_ability_exist(AbilityID.SUSTAIN_DAMAGE)

    def to_save_dict(self) -> dict:
        d  = ConfigBoundStateObj[UnitConfig].to_save_dict(self)
        d |= TextBoundStateObjMixin[FunctionalTextConfig].to_save_dict(self)
        d |= PlayerOwnable.to_save_dict(self)
        return d | {
            "location": self.location.to_save_dict(),
            "current_damage": self.current_damage,
            "sustainable_damage": self._sustainable_damage,
        }

    @classmethod
    def from_save_dict(cls, config: UnitConfig, text_config: FunctionalTextConfig, location: dict, **kwargs):
        return cls(
            config=config,
            text_config=text_config,
            location=UnitLocation.from_save_dict(**location),
            **kwargs
        )