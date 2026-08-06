from dataclasses import dataclass, field
from collections.abc import Iterable
from types import MappingProxyType
from pathlib import Path
from typing import Self

from app.config.shared import IDConfigObj
from app.config.text_objs.base import BaseTextConfigObj

from .loader import *

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

from .text_objs import (
    ActionTextConfig,
    ActionCardTextConfig,
    AgendaTextConfig,
    ObjectiveCardTextConfig,
    PlanetTextConfig,
    PromissoryNoteTextConfig,
    StrategyCardTextConfig,
    TechTextConfig,
    UnitTextConfig
)

from .setup import SetupConfig

@dataclass(slots=True, frozen=True)
class ConfigAndTextObj[TConfig: IDConfigObj, TTextConfig: BaseTextConfigObj]:
    config: TConfig
    text_config: TTextConfig

def _sort_configs_and_text_configs(configs: Iterable[IDConfigObj], text_configs: Iterable[BaseTextConfigObj]) -> dict[str, ConfigAndTextObj]:
    configs_and_text_configs = {}
    for config in configs:
        configs_and_text_configs[config.id] = ConfigAndTextObj(config, next(filter(lambda cfg: cfg.id == config.id, text_configs)))
    return configs_and_text_configs

@dataclass(slots=True, frozen=True)
class RulesetConfig:
    abilities: MappingProxyType[str, ConfigAndTextObj[AbilityConfig, ActionTextConfig]] = field(default_factory=dict)
    action_cards: MappingProxyType[str, ConfigAndTextObj[ActionCardConfig, ActionCardTextConfig]] = field(default_factory=dict)
    agendas: MappingProxyType[str, ConfigAndTextObj[AgendaConfig, AgendaTextConfig]] = field(default_factory=dict)
    factions: MappingProxyType[str, FactionConfig] = field(default_factory=dict)
    maps: MappingProxyType[str, MapConfig] = field(default_factory=dict)
    objectives: MappingProxyType[str, ConfigAndTextObj[ObjectiveConfig, ObjectiveCardTextConfig]] = field(default_factory=dict)
    planets: MappingProxyType[str, ConfigAndTextObj[PlanetConfig, PlanetTextConfig]] = field(default_factory=dict)
    promissory_notes: MappingProxyType[str, ConfigAndTextObj[PromissoryNoteConfig, PromissoryNoteTextConfig]] = field(default_factory=dict)
    setup: MappingProxyType[str, SetupConfig] = field(default_factory=dict)
    strategy_cards: MappingProxyType[str, ConfigAndTextObj[StrategyCardConfig, StrategyCardTextConfig]] = field(default_factory=dict)
    systems: MappingProxyType[str, SystemConfig] = field(default_factory=dict)
    techs: MappingProxyType[str, ConfigAndTextObj[TechConfig, TechTextConfig]] = field(default_factory=dict)
    units: MappingProxyType[str, ConfigAndTextObj[UnitConfig, UnitTextConfig]] = field(default_factory=dict)

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
            abilities = _sort_configs_and_text_configs(load_ability_data(config_dir / "objs" / "abilities.yaml", config_dir / "text_objs" / "abilities.yaml")),
            action_cards = _sort_configs_and_text_configs(load_action_card_data(config_dir / "objs" / "action_cards.yaml", config_dir / "text_objs" / "action_cards.yaml")),
            agendas = _sort_configs_and_text_configs(load_agenda_data(config_dir / "objs" / "agendas.yaml", config_dir / "text_objs" / "agendas.yaml")),
            factions = {faction.id: faction for faction in load_faction_data(config_dir / "objs" / "factions.yaml")},
            maps = {map.id: map for map in load_map_data([config_dir / "objs" / "maps" / "triangular.yaml", config_dir / "objs" / "maps" / "standard.yaml"])},
            objectives = _sort_configs_and_text_configs(load_objective_data(config_dir / "objs" / "objectives.yaml", config_dir / "text_objs" / "objectives.yaml")),
            planets = _sort_configs_and_text_configs(load_planet_data(config_dir / "objs" / "planets.yaml", config_dir / "text_objs" / "planets.yaml")),
            promissory_notes = _sort_configs_and_text_configs(load_promissory_note_data(config_dir / "objs" / "promissory_notes.yaml", config_dir / "text_objs" / "promissory_notes.yaml")),
            setup = {setup.id: setup for setup in load_setup_data(config_dir / "setup.yaml")},
            strategy_cards = _sort_configs_and_text_configs(load_strategy_card_data(config_dir / "objs" / "strategy_cards.yaml", config_dir / "text_objs" / "strategy_cards.yaml")),
            systems = {system.id: system for system in load_system_data(config_dir / "objs" / "systems.yaml")},
            techs = _sort_configs_and_text_configs(load_tech_data(config_dir / "objs" / "techs.yaml", config_dir / "text_objs" / "techs.yaml")),
            units = _sort_configs_and_text_configs(load_unit_data(config_dir / "objs" / "units.yaml", config_dir / "text_objs" / "units.yaml"))
        )
