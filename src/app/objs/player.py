
from typing import Iterable
import dataclasses as dc

from .named import NamedObject

type Planet = Planet
type Faction = Faction
type StrategyCard = StrategyCard
type ActionCard = ActionCard
type ObjectiveCard = ObjectiveCard
type Tech = Tech
type Unit = Unit
type Objective = Objective

_MAX_CONTROL_TOKENS = 17
_MAX_COMMAND_TOKENS = 16

_MAX_SPACE_DOCKS = 3
_MAX_PDS = 6
_MAX_DESTROYERS = 8
_MAX_CRUISERS = 8
_MAX_WAR_SUNS = 2
_MAX_INF_TOKENS = 12
_MAX_FIGHTER_TOKENS = 10
_MAX_CARRIERS = 4
_MAX_DREADNOUGHTS = 5
_MAX_FLAGSHIPS = 1

@dc.dataclass(slots=True)
class Player(NamedObject):
    name: str = dc.InitVar[str]
    speaker: bool = False
    faction: Faction = None
    strategy_card: StrategyCard = None
    action_cards: list[ActionCard] = dc.field(default_factory=list)
    objective_cards: list[ObjectiveCard] = dc.field(default_factory=list)
    planets: set[Planet] = dc.field(default_factory=set)
    techs: set[Tech] = dc.field(default_factory=set)
    units_deployed: dict[str: list[Unit]] = dc.field(default_factory=dict)
    commodoties: int = 0
    trade_goods: int = 0
    victory_pts: int = 0
    
    _techs_avail: set[Tech] = dc.field(default_factory=set)
    _unit_pool: dict[str: int] = dc.field(default_factory=dict)
    _control_token_pool: int = _MAX_CONTROL_TOKENS
    _command_token_pool: int = _MAX_COMMAND_TOKENS
    
    def __post_init__(self, name: str) -> None:
        NamedObject.__init__(self, name)

    def become_speaker(self):
        self.speaker = True
    
    def gain_planets(self, planets: Iterable[Planet]) -> None:
        self.planets.update(planets)

    def has_planets(self, planets: Iterable[Planet]) -> bool:
        return self.planets.issuperset(planets)
    
    def has_planet(self, planet: Planet) -> bool:
        return planet in self.planets