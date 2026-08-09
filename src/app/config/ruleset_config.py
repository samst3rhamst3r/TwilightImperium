from dataclasses import dataclass, field
from types import MappingProxyType
from pathlib import Path
from typing import Self

from .yaml_loader import *

from .objs.ability import AbilityConfig
from .objs.action_card import ActionCardConfig
from .objs.agenda import AgendaConfig
from .objs.faction import FactionConfig
from .objs.map import MapConfig
from .objs.objective import ObjectiveConfig
from .objs.planet import PlanetConfig
from .objs.promissory_note import PromissoryNoteConfig
from .objs.strategy_card import StrategyCardConfig
from .objs.system import SystemConfig
from .objs.tech import TechConfig
from .objs.unit import UnitConfig

from .setup import SetupConfig

@dataclass(slots=True, frozen=True)
class RulesetConfig:
    abilities: MappingProxyType[str, AbilityConfig] = field(default_factory=dict)
    action_cards: MappingProxyType[str, ActionCardConfig] = field(default_factory=dict)
    agendas: MappingProxyType[str, AgendaConfig] = field(default_factory=dict)
    factions: MappingProxyType[str, FactionConfig] = field(default_factory=dict)
    maps: MappingProxyType[str, MapConfig] = field(default_factory=dict)
    objectives: MappingProxyType[str, ObjectiveConfig] = field(default_factory=dict)
    planets: MappingProxyType[str, PlanetConfig] = field(default_factory=dict)
    promissory_notes: MappingProxyType[str, PromissoryNoteConfig] = field(default_factory=dict)
    setup: MappingProxyType[str, SetupConfig] = field(default_factory=dict)
    strategy_cards: MappingProxyType[str, StrategyCardConfig] = field(default_factory=dict)
    systems: MappingProxyType[str, SystemConfig] = field(default_factory=dict)
    techs: MappingProxyType[str, TechConfig] = field(default_factory=dict)
    units: MappingProxyType[str, UnitConfig] = field(default_factory=dict)

    def __post_init__(self):
        object.__setattr__(self, "abilities", MappingProxyType(self.abilities))
        object.__setattr__(self, "action_cards", MappingProxyType(self.action_cards))
        object.__setattr__(self, "agendas", MappingProxyType(self.agendas))
        object.__setattr__(self, "factions", MappingProxyType(self.factions))
        object.__setattr__(self, "maps", MappingProxyType(self.maps))
        object.__setattr__(self, "objectives", MappingProxyType(self.objectives))
        object.__setattr__(self, "planets", MappingProxyType(self.planets))
        object.__setattr__(self, "promissory_notes", MappingProxyType(self.promissory_notes))
        object.__setattr__(self, "setup", MappingProxyType(self.setup))
        object.__setattr__(self, "strategy_cards", MappingProxyType(self.strategy_cards))
        object.__setattr__(self, "systems", MappingProxyType(self.systems))
        object.__setattr__(self, "techs", MappingProxyType(self.techs))
        object.__setattr__(self, "units", MappingProxyType(self.units))

    @classmethod
    def load(cls, config_dir: Path) -> Self:
        
        return cls(
            abilities = {ability.id: ability for ability in load_ability_data(config_dir)},
            action_cards = {action_card.id: action_card for action_card in load_action_card_data(config_dir)},
            agendas = {agendum.id: agendum for agendum in load_agenda_data(config_dir)},
            factions = {faction.id: faction for faction in load_faction_data(config_dir)},
            maps = {map.id: map for map in load_map_data(config_dir)},
            objectives = {objective.id: objective for objective in load_objective_data(config_dir)},
            planets = {planet.id: planet for planet in load_planet_data(config_dir)},
            promissory_notes = {promissory_note.id: promissory_note for promissory_note in load_promissory_note_data(config_dir)},
            setup = {setup.id: setup for setup in load_setup_data(config_dir)},
            strategy_cards = {strategy_card.id: strategy_card for strategy_card in load_strategy_card_data(config_dir)},
            systems = {system.id: system for system in load_system_data(config_dir)},
            techs = {tech.id: tech for tech in load_tech_data(config_dir)},
            units = {unit.id: unit for unit in load_unit_data(config_dir)},
        )
