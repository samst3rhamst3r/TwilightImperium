from dataclasses import dataclass
from types import MappingProxyType
from pathlib import Path
from typing import Self

from .objs.ability import AbilityConfig, load_ability_data
from .objs.action_card import ActionCardConfig, load_action_card_data
from .objs.agenda import AgendaConfig, load_agenda_data
from .objs.faction import FactionConfig, load_faction_data
from .objs.map import MapConfig, load_map_data
from .objs.objective import ObjectiveConfig, load_objective_data
from .objs.planet import PlanetConfig, load_planet_data
from .objs.promissory_note import PromissoryNoteConfig, load_promissory_note_data
from .objs.strategy_card import StrategyCardConfig, load_strategy_card_data
from .objs.system import SystemConfig, load_system_data
from .objs.tech import TechConfig, load_tech_data
from .objs.unit import UnitConfig, load_unit_data

@dataclass(frozen=True, kw_only=True)
class RulesetConfig:
    abilities: MappingProxyType[str, AbilityConfig]
    action_cards: MappingProxyType[str, ActionCardConfig]
    agendas: MappingProxyType[str, AgendaConfig]
    factions: MappingProxyType[str, FactionConfig]
    maps: MappingProxyType[str, MapConfig]
    objectives: MappingProxyType[str, ObjectiveConfig]
    planets: MappingProxyType[str, PlanetConfig]
    promissory_notes: MappingProxyType[str, PromissoryNoteConfig]
    strategy_cards: MappingProxyType[str, StrategyCardConfig]
    systems: MappingProxyType[str, SystemConfig]
    techs: MappingProxyType[str, TechConfig]
    units: MappingProxyType[str, UnitConfig]

    @classmethod
    def load(cls, config_dir: Path) -> Self:
        
        return cls(
            abilities = MappingProxyType({ability.id: ability for ability in load_ability_data(config_dir)}),
            action_cards = MappingProxyType({action_card.id: action_card for action_card in load_action_card_data(config_dir)}),
            agendas = MappingProxyType({agendum.id: agendum for agendum in load_agenda_data(config_dir)}),
            factions = MappingProxyType({faction.id: faction for faction in load_faction_data(config_dir)}),
            maps = MappingProxyType({map.id: map for map in load_map_data(config_dir)}),
            objectives = MappingProxyType({objective.id: objective for objective in load_objective_data(config_dir)}),
            planets = MappingProxyType({planet.id: planet for planet in load_planet_data(config_dir)}),
            promissory_notes = MappingProxyType({promissory_note.id: promissory_note for promissory_note in load_promissory_note_data(config_dir)}),
            strategy_cards = MappingProxyType({strategy_card.id: strategy_card for strategy_card in load_strategy_card_data(config_dir)}),
            systems = MappingProxyType({system.id: system for system in load_system_data(config_dir)}),
            techs = MappingProxyType({tech.id: tech for tech in load_tech_data(config_dir)}),
            units = MappingProxyType({unit.id: unit for unit in load_unit_data(config_dir)}),
        )
