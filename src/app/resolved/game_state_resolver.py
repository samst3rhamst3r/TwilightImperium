

from collections.abc import Mapping
from typing import ClassVar

from app.config.ruleset_config import RulesetConfig
from app.errors import GameError
from app.state.game import GameState

from .player import ResolvedPlayer
from .unit import ResolvedUnit
from .planet import ResolvedPlanet
from .system import ResolvedSystem

class UnknownEntityError(GameError):
    """Raised when an entity ID doesn't resolve to any entity in the current game."""
    entity_type: ClassVar[str] = "entity"

    def __init__(self, entity_id: str):
        super().__init__(f"No {self.entity_type} with id {entity_id!r} exists in this game.")

class UnknownPlayerError(UnknownEntityError):
    """Raised when player_id doesn't resolve to any player in the current game."""
    entity_type: ClassVar[str] = "player"

class UnknownDeployedUnitError(UnknownEntityError):
    """Raised when unit_id doesn't resolve to any unit in the current game."""
    entity_type: ClassVar[str] = "deployed unit"

class UnknownUnitConfigError(UnknownEntityError):
    """Raised when unit_id doesn't resolve to any unit in the current game."""
    entity_type: ClassVar[str] = "unit config"

class UnknownSystemStateError(UnknownEntityError):
    """Raised when destination_system_id doesn't resolve to any system in the current game."""
    entity_type: ClassVar[str] = "system state object"

class UnknownSystemConfigError(UnknownEntityError):
    """Raised when system_id doesn't resolve to any system config in the current game."""
    entity_type: ClassVar[str] = "system config"

class UnknownPlanetStateError(UnknownEntityError):
    """Raised when planet_id doesn't resolve to any planet in the current game."""
    entity_type: ClassVar[str] = "planet state object"

class UnknownPlanetConfigError(UnknownEntityError):
    """Raised when planet_id doesn't resolve to any planet in the current game."""
    entity_type: ClassVar[str] = "planet config"

class UnknownFactionError(UnknownEntityError):
    """Raised when faction_config_id doesn't resolve to any faction in the current game."""
    entity_type: ClassVar[str] = "faction config"

class GameStateResolver:

    def __init__(self, game_state: GameState, ruleset_config: RulesetConfig):
        self._game_state = game_state
        self._ruleset_config = ruleset_config

    def _get[T](self, entity_dict: Mapping[str, T], entity_id: str, error_cls: type[UnknownEntityError]) -> T:
        try:
            return entity_dict[entity_id]
        except KeyError:
            raise error_cls(entity_id) from None

    def resolved_player(self, player_id: str) -> ResolvedPlayer:
        player_state = self._get(self._game_state.players, player_id, UnknownPlayerError)
        faction_config = self._get(self._ruleset_config.factions, player_state.faction_config_id, UnknownFactionError)
        return ResolvedPlayer(player_state, faction_config)

    def resolved_unit(self, unit_id: str) -> ResolvedUnit:
        unit_state = self._get(self._game_state.deployed_units, unit_id, UnknownDeployedUnitError)
        unit_config = self._get(self._ruleset_config.units, unit_state.config_id, UnknownUnitConfigError)
        return ResolvedUnit(unit_state, unit_config)

    def resolved_planet(self, planet_id: str) -> ResolvedPlanet:
        planet_state = self._get(self._game_state.planets, planet_id, UnknownPlanetStateError)
        planet_config = self._get(self._ruleset_config.planets, planet_state.config_id, UnknownPlanetConfigError)
        return ResolvedPlanet(planet_state, planet_config)

    def resolved_system(self, system_id: str) -> ResolvedSystem:
        system_state = self._get(self._game_state.systems, system_id, UnknownSystemStateError)
        system_config = self._get(self._ruleset_config.systems, system_state.config_id, UnknownSystemConfigError)
        return ResolvedSystem(system_state, system_config)