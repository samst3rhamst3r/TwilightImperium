from dataclasses import dataclass
from typing import Self

from app.state.base import PlayerOwnableWithConvenienceProtocol

@dataclass(kw_only=True)
class NaaluTokenState(PlayerOwnableWithConvenienceProtocol):

    @classmethod
    def new_game(cls, player_id: str) -> Self:
        obj = cls()
        obj.assign_owner(player_id)
        return obj
