from dataclasses import dataclass
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

@dataclass(slots=True, frozen=True, kw_only=True)
class RulesetConfig:
    abilities: MappingProxyType[str, AbilityConfig]
    action_cards: MappingProxyType[str, ActionCardConfig]
    agendas: MappingProxyType[str, AgendaConfig]
    factions: MappingProxyType[str, FactionConfig]
    maps: MappingProxyType[str, MapConfig]
    objectives: MappingProxyType[str, ObjectiveConfig]
    planets: MappingProxyType[str, PlanetConfig]
    promissory_notes: MappingProxyType[str, PromissoryNoteConfig]
    setup: tuple[SetupConfig, ...] = ()
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
            setup = tuple(load_setup_data(config_dir)),
            strategy_cards = MappingProxyType({strategy_card.id: strategy_card for strategy_card in load_strategy_card_data(config_dir)}),
            systems = MappingProxyType({system.id: system for system in load_system_data(config_dir)}),
            techs = MappingProxyType({tech.id: tech for tech in load_tech_data(config_dir)}),
            units = MappingProxyType({unit.id: unit for unit in load_unit_data(config_dir)}),
        )
