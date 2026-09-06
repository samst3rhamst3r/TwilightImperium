from app.resolved.game_state_resolver import GameStateResolver
from app.state.base.ownable import OwnableEntity, OwnershipError

class BaseService:

    def __init__(self, resolver: GameStateResolver):
        self._resolver = resolver

    def _require_ownership(self, entity: OwnableEntity, player_id: str, error_cls: type[OwnershipError]) -> None:
        if not entity.ownable.is_owned_by_player(player_id):
            raise error_cls(entity.id, entity.ownable.owned_by_player_id)
