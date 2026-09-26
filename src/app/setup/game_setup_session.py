from dataclasses import dataclass, field
from typing import Final, TypedDict
from enum import Enum, auto
from pathlib import Path
from abc import abstractmethod, ABC

from app.config.player_color import PlayerColor
from app.config.setup import SetupConfig
from app.config.yaml_loader import load_first_game_system_tile_mapping, load_setup_data
from app.geometry.coordinate import HexCoordinate
from app.setup.game_setup import NewGameSetup

class PlayerDoesNotExistError(Exception):
    pass

class PlayerAlreadyExistsError(Exception):
    pass

class InvalidGameSetupError(Exception):
    pass

class _PlayerStateInfo(TypedDict):
    name: str
    color: PlayerColor
    faction_config_id: str

_MIN_PLAYERS: Final[int] = 3
_MAX_PLAYERS: Final[int] = 6
_STANDARD_VICTORY_POINT_THRESHOLD: Final[int] = 10
_ADVANCED_VICTORY_POINT_THRESHOLD: Final[int] = 14

_ROOT_SETUP_YAML_PATH: Final[Path] = Path(__file__).parent.parent.parent.resolve() / "data"

class _SetupPhase(Enum):
    """The phases of a game setup session."""
    JOINING = auto()
    ROSTER_LOCKED = auto()

@dataclass(slots=True)
class NewGameSetupSession(ABC):
    """A session for setting up a new game, containing all the information needed to start a game."""
    players: dict[str, _PlayerStateInfo] = field(default_factory=dict)
    speaker_id: str | None = None
    system_placements: dict[HexCoordinate, str] = field(default_factory=dict) # Hex Coordinates should be key, because the map shape has no null values
    victory_point_threshold: int = field(init=False, default=_STANDARD_VICTORY_POINT_THRESHOLD)

    _phase: _SetupPhase = field(init=False, default=_SetupPhase.JOINING)
    _setup_config: SetupConfig | None = field(init=False, default=None)

    @property
    def player_names(self) -> list[str]:
        """Return a list of player names in the game setup session."""
        return list(self.players.keys())

    @property
    def num_players(self) -> int:
        """Return the number of players in the game setup session."""
        return len(self.players)

    def rename_player(self, old_name: str, new_name: str) -> None:
        """Rename a player in the game setup session."""
        if self._phase is not _SetupPhase.JOINING:
            raise InvalidGameSetupError("Cannot rename a player after the roster has been confirmed.")
        if old_name not in self.players:
            raise PlayerDoesNotExistError(f"'{old_name}' is not in the list of players.")
        if new_name in self.players:
            raise PlayerAlreadyExistsError(f"Player with name {new_name} already exists.")
        self.players[new_name] = self.players.pop(old_name)
        self.players[new_name]['name'] = new_name
        if self.speaker_id == old_name:
            self.speaker_id = new_name

    def add_new_player(self, player_name: str) -> None:
        """Add a player to the game setup session."""
        if self._phase is not _SetupPhase.JOINING:
            raise InvalidGameSetupError("Cannot add a player after the roster has been confirmed.")
        if player_name in self.players:
            raise PlayerAlreadyExistsError(f"Player with name {player_name} already exists.")
        self.players[player_name] = _PlayerStateInfo(name=player_name)

    def add_player_color(self, player_name: str, player_color: PlayerColor) -> None:
        """Add a player's color to the game setup session."""
        if self._phase is not _SetupPhase.JOINING:
            raise InvalidGameSetupError("Cannot add a player's color after the roster has been confirmed.")
        if player_name not in self.players:
            self.add_new_player(player_name)
        self.players[player_name]['color'] = player_color

    def add_player_faction(self, player_name: str, faction_config_id: str) -> None:
        """Add a player's faction to the game setup session."""
        if self._phase is not _SetupPhase.JOINING:
            raise InvalidGameSetupError("Cannot add a player's faction after the roster has been confirmed.")
        if player_name not in self.players:
            self.add_new_player(player_name)
        self.players[player_name]['faction_config_id'] = faction_config_id

    def confirm_roster(self) -> None:
        """Confirm the roster of players and move to the next phase of the game setup session."""
        if len(self.players) < _MIN_PLAYERS:
            raise InvalidGameSetupError(f"A game must have at least {_MIN_PLAYERS} players.")
        if len(self.players) > _MAX_PLAYERS:
            raise InvalidGameSetupError(f"A game can have at most {_MAX_PLAYERS} players.")
        if self._phase is _SetupPhase.ROSTER_LOCKED:
            raise InvalidGameSetupError("Roster has already been confirmed.")
        self._phase = _SetupPhase.ROSTER_LOCKED

        self._setup_config = load_setup_data(_ROOT_SETUP_YAML_PATH, self.num_players)

    @abstractmethod
    def finalize(self):
        """Finalize the game setup session and return a NewGameSetup object."""
        if self._phase is not _SetupPhase.ROSTER_LOCKED:
            raise InvalidGameSetupError("Cannot finalize the game setup session before the roster has been confirmed.")
        empty_tiles = [hex_tile for hex_tile, system_id in self.system_placements.items() if system_id is None]
        if empty_tiles:
            raise InvalidGameSetupError(f"Cannot finalize the game setup session with unplaced systems at hex coordinates: {empty_tiles}")
        return NewGameSetup(
            players=list(self.players.keys()),
            system_placements=self.system_placements,
            planets=self.planets,
            victory_point_threshold=self.victory_point_threshold,
        )

    def assign_speaker(self, player_name: str) -> None:
        """Assign the speaker for the start of the game."""
        if player_name not in self.players:
            raise PlayerDoesNotExistError(f"'{player_name}' is not in the list of players.")
        self.speaker_id = player_name

    def place_home_system(self, system_id: str, hex_coordinate: HexCoordinate) -> None:
        """Place a player's home system at the given hex coordinate."""

        if self._phase is not _SetupPhase.ROSTER_LOCKED:
            raise InvalidGameSetupError("Cannot place a home system before the roster has been confirmed.")

        valid = False
        for expected_home_coordinate in self._setup_config.player_setup:
            if expected_home_coordinate.home_system_coordinates == hex_coordinate:
                valid = True
                break
        if not valid:
            raise InvalidGameSetupError(f"Hex coordinate {hex_coordinate} is not a valid home system coordinate. Valid coordinates are: {[setup.home_system_coordinates for setup in self._setup_config.player_setup]}")
        
        if self.system_placements[hex_coordinate] is not None:
            raise InvalidGameSetupError(f"Hex coordinate {hex_coordinate} is already occupied by system {self.system_placements[hex_coordinate]}.")
        
        self.system_placements[hex_coordinate] = system_id

    def _validate(self):
        """Validate the game setup session."""
        if len(self.players) < _MIN_PLAYERS:
            raise InvalidGameSetupError(f"A game must have at least {_MIN_PLAYERS} players.")
        if len(self.players) > _MAX_PLAYERS:
            raise InvalidGameSetupError(f"A game can have at most {_MAX_PLAYERS} players.")
        if self.speaker_id is None:
            raise InvalidGameSetupError("Speaker has not been assigned.")

class FirstGameSetupSession(NewGameSetupSession):
    """A session for setting up a new game, containing all the information needed to start a game."""

    def confirm_roster(self) -> None:
        """Confirm the roster of players and move to the next phase of the game setup session."""
        super().confirm_roster()
        self.system_placements = {
            HexCoordinate(*hex_tile): system_id for hex_tile, system_id in zip(
                self._setup_config.map_config.tiles,
                load_first_game_system_tile_mapping(_ROOT_SETUP_YAML_PATH, self.num_players)
            )
        }

    def finalize(self) -> None:
        self._validate()
        tiles = load_first_game_system_tile_mapping(_ROOT_SETUP_YAML_PATH, self.num_players)
        hex_coordinates = [HexCoordinate(*tile) for tile in tiles if tile is not None]

class AdvancedGameSetupSession(NewGameSetupSession):
    """A session for setting up a new game, containing all the information needed to start a game."""

    def choose_standard_victory_point_threshold(self) -> None:
        self.victory_point_threshold = _STANDARD_VICTORY_POINT_THRESHOLD

    def choose_advanced_victory_point_threshold(self) -> None:
        self.victory_point_threshold = _ADVANCED_VICTORY_POINT_THRESHOLD

    def place_system(self, system_id: str, hex_coordinate: HexCoordinate) -> None:
        """Place a system at the given hex coordinate."""
        self.system_placements[hex_coordinate] = system_id
