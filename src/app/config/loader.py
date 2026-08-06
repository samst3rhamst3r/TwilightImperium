from yaml import safe_load
from typing import Any
from collections.abc import Iterable
from pathlib import Path

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

def _load_data(config_path: Path) -> Any:
    with open(config_path) as f:
        return safe_load(f)

def load_ability_data(config_path: Path, text_config_path: Path) -> tuple[tuple[AbilityConfig, ...], tuple[ActionTextConfig, ...]]:
    return tuple(AbilityConfig(**config) for config in _load_data(config_path)), tuple(ActionTextConfig(**text_config) for text_config in _load_data(text_config_path))

def load_action_card_data(config_path: Path, text_config_path: Path) -> tuple[tuple[ActionCardConfig, ...], tuple[ActionCardTextConfig, ...]]:
    return tuple(ActionCardConfig(**config) for config in _load_data(config_path)), tuple(ActionCardTextConfig(**text_config) for text_config in _load_data(text_config_path))

def load_agenda_data(config_path: Path, text_config_path: Path) -> tuple[tuple[AgendaConfig, ...], tuple[AgendaTextConfig, ...]]:
    return tuple(AgendaConfig(**config) for config in _load_data(config_path)), tuple(AgendaTextConfig(**text_config) for text_config in _load_data(text_config_path))

def load_faction_data(config_path: Path) -> tuple[FactionConfig, ...]:
    return tuple(FactionConfig(**config) for config in _load_data(config_path))

def load_map_data(config_paths: Iterable[Path]) -> tuple[MapConfig, ...]:
    return tuple(_load_data(path) for path in config_paths)

def load_setup_data(config_path: Path) -> tuple[SetupConfig, ...]:
    return tuple(SetupConfig(**config) for config in _load_data(config_path))

def load_objective_data(config_path: Path, text_config_path: Path) -> tuple[tuple[ObjectiveConfig], tuple[ObjectiveCardTextConfig]]:
    return tuple(ObjectiveConfig(**config) for config in _load_data(config_path)), tuple(ObjectiveCardTextConfig(**text_config) for text_config in _load_data(text_config_path))

def load_planet_data(config_path: Path, text_config_path: Path) -> tuple[tuple[PlanetConfig], tuple[PlanetTextConfig]]:
    return tuple(PlanetConfig(**config) for config in _load_data(config_path)), tuple(PlanetTextConfig(**text_config) for text_config in _load_data(text_config_path))

def load_promissory_note_data(config_path: Path, text_config_path: Path) -> tuple[tuple[PromissoryNoteConfig], tuple[PromissoryNoteTextConfig]]:
    return tuple(PromissoryNoteConfig(**config) for config in _load_data(config_path)), tuple(PromissoryNoteTextConfig(**text_config) for text_config in _load_data(text_config_path))

def load_strategy_card_data(config_path: Path, text_config_path: Path) -> tuple[tuple[StrategyCardConfig], tuple[StrategyCardTextConfig]]:
    return tuple(StrategyCardConfig(**config) for config in _load_data(config_path)), tuple(StrategyCardTextConfig(**text_config) for text_config in _load_data(text_config_path))

def load_system_data(config_path: Path) -> tuple[SystemConfig]:
    return tuple(SystemConfig(**config) for config in _load_data(config_path))

def load_tech_data(config_path: Path, text_config_path: Path) -> tuple[tuple[TechConfig], tuple[TechTextConfig]]:
    return tuple(TechConfig(**config) for config in _load_data(config_path)), tuple(TechTextConfig(**text_config) for text_config in _load_data(text_config_path))

def load_unit_data(config_path: Path, text_config_path: Path) -> tuple[tuple[UnitConfig], tuple[UnitTextConfig]]:
    return tuple(UnitConfig(**config) for config in _load_data(config_path)), tuple(UnitTextConfig(**text_config) for text_config in _load_data(text_config_path))
