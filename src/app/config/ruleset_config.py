from dataclasses import dataclass
from types import MappingProxyType
from pathlib import Path
from typing import Self

from .objs.ability import AbilityConfig, load_ability_data
from .objs.action_card import ActionCardConfig, load_action_card_data
from .objs.agenda import AgendaConfig, load_agenda_data
from .objs.faction import FactionConfig, load_faction_data
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
            abilities = load_ability_data(config_dir),
            action_cards = load_action_card_data(config_dir),
            agendas = load_agenda_data(config_dir),
            factions = load_faction_data(config_dir),
            objectives = load_objective_data(config_dir),
            planets = load_planet_data(config_dir),
            promissory_notes = load_promissory_note_data(config_dir),
            strategy_cards = load_strategy_card_data(config_dir),
            systems = load_system_data(config_dir),
            techs = load_tech_data(config_dir),
            units = load_unit_data(config_dir),
        )
