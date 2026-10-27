from dataclasses import dataclass

from app.state.base import PlayerOwnableMixin

@dataclass(kw_only=True)
class SpeakerTokenState(PlayerOwnableMixin):

    def assign_speaker(self, player_id: str) -> None:
        self.ownable.assign_owner(player_id)

    def reassign_speaker(self, player_id: str) -> str:
        return self.ownable.reassign_owner(player_id)

    def release_speaker(self) -> str:
        return self.ownable.release_owner()

    def is_player_speaker(self, player_id: str) -> bool:
        return self.ownable.is_owned_by_player(player_id)

    @property
    def speaker_player_id(self) -> str | None:
        return self.ownable.owned_by_player_id
