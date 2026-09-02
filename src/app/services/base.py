from app.resolved.game_state_resolver import GameStateResolver

class BaseService:

    def __init__(self, resolver: GameStateResolver):
        self._resolver = resolver
