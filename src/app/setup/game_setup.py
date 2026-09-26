from dataclasses import dataclass

from app.config.player_color import PlayerColor

@dataclass(slots=True, frozen=True, kw_only=True)
class _PlayerStateInfo:
    color: PlayerColor
    name: str
    faction_config_id: str

@dataclass(slots=True, frozen=True, kw_only=True)
class NewGameSetup:
    """The final state of a game setup session, containing all the information needed to start a game."""
    players: list[str]
    systems: list[str]
    planets: list[str]

    def __post_init__(self):
        if len(self.players) < 3:
            raise ValueError("A game must have at least 3 players.")
        if len(self.players) > 6:
            raise ValueError("A game can have at most 6 players.")