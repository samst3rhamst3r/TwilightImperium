from app.config.ruleset_config import RulesetConfig
from app.state.game import GameState

from .player import ResolvedPlayer
from .unit import ResolvedUnit
from .planet import ResolvedPlanet

class GameStateResolver:

    def __init__(self, game_state: GameState, ruleset_config: RulesetConfig):
        self._game_state = game_state
        self._ruleset_config = ruleset_config

    def resolved_player(self, player_id: str) -> ResolvedPlayer:
        player_state = self._game_state.players[player_id]
        faction_config = self._ruleset_config.factions[player_state.faction_config_id]
        return ResolvedPlayer(player_state, faction_config)

    def resolved_unit(self, unit_id: str) -> ResolvedUnit:
        unit_state = self._game_state.deployed_units[unit_id]
        unit_config = self._ruleset_config.units[unit_state.config_id]
        return ResolvedUnit(unit_state, unit_config)

    def resolved_planet(self, planet_id: str) -> ResolvedPlanet:
        planet_state = self._game_state.planets[planet_id]
        planet_config = self._ruleset_config.planets[planet_state.config_id]
        return ResolvedPlanet(planet_state, planet_config)