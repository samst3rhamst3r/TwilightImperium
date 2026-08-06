from dataclasses import dataclass, field
from collections.abc import Iterable

from .loader import *

from .ability import AbilityConfig
from .action_card import ActionCardConfig
from .agenda import AgendaConfig
from .faction import FactionConfig
from .objective import ObjectiveConfig
from .planet import PlanetConfig
from .promissory_note import PromissoryNoteConfig
from .setup import SetupConfig
from .strategy_card import StrategyCardConfig
from .system import SystemConfig
from .tech import TechConfig
from .unit import UnitConfig

@dataclass(slots=True, frozen=True)
class RulesetConfig:
    ability_data: list[dict[str, Any]] = field(default_factory=list)

    @classmethod
    def new_game(cls, num_players: int)