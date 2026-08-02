
from typing import Iterable
from dataclasses import dataclass, field

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

@dataclass(slots=True)
class Player:
    name: str
    speaker: bool = False
    faction: Faction = None
    strategy_card: StrategyCard = None
    action_cards: list[ActionCard] = field(default_factory=list)
    objective_cards: list[ObjectiveCard] = field(default_factory=list)
    planets: set[Planet] = field(default_factory=set)
    techs: set[Tech] = field(default_factory=set)
    units_deployed: dict[str: list[Unit]] = field(default_factory=dict)
    commodoties: int = 0
    trade_goods: int = 0
    victory_pts: int = 0
    
    _techs_avail: set[Tech] = field(default_factory=set)
    _unit_pool: dict[str: int] = field(default_factory=dict)
    _control_token_pool: int = _MAX_CONTROL_TOKENS
    _command_token_pool: int = _MAX_COMMAND_TOKENS
    
    def become_speaker(self):
        self.speaker = True
    
    def gain_planets(self, planets: Iterable[Planet]) -> None:
        self.planets.update(planets)

    def has_planets(self, planets: Iterable[Planet]) -> bool:
        return self.planets.issuperset(planets)
    
    def has_planet(self, planet: Planet) -> bool:
        return planet in self.planets