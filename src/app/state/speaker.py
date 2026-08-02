from dataclasses import dataclass

from .shared.ownable import PlayerOwnable

@dataclass(slots=True, kw_only=True)
class SpeakerState(PlayerOwnable):

    def assign_speaker(self, player_id: str) -> None:
        self.assign_owner(player_id)

    def reassign_speaker(self, player_id: str) -> str:
        return self.reassign_owner(player_id)

    def release_speaker(self) -> str:
        return self.release_owner()

    def is_player_speaker(self, player_id: str) -> bool:
        return self.is_owned_by_player(player_id)
    