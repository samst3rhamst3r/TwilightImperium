from dataclasses import dataclass, field
from collections.abc import Iterable
from types import MappingProxyType

from .loader import *

from .objs.ability import AbilityConfig
from .objs.action_card import ActionCardConfig
from .objs.agenda import AgendaConfig
from .objs.faction import FactionConfig
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
    ability_registry: MappingProxyType[str, AbilityConfig] = field(default_factory=dict)

    def __post_init__(self):
        object.__setattr__(self, "ability_registry", MappingProxyType({self.ability_registry}))