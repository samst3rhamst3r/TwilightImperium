from .base import BaseService

from app.errors import GameError
from app.state.unit import UnitOwnershipError

class MovementError(GameError):
    """Base for every rejection MovementService.move_unit can raise."""

class SelfMoveError(MovementError):
    """Raised when the requested destination is the unit's own current system."""

class IllegalDestinationError(MovementError):
    """Raised when the destination is a real, different system, but isn't a
    direct hex neighbor of the unit's current system - the only legal-
    destination source this feature recognizes."""

class MovementService(BaseService):

    def move_unit(
        self,
        *,
        unit_id: str,
        destination_system_id: str,
        requesting_player_id: str,
    ) -> None:

        resolved_unit = self._resolver.resolved_unit(unit_id)
        destination_system = self._resolver.resolved_system(destination_system_id)

        self._require_ownership(resolved_unit.state, requesting_player_id, UnitOwnershipError)

        origin_system_id = resolved_unit.state.location.location_id
        if destination_system_id == origin_system_id:
            raise SelfMoveError(
                f"Unit {unit_id!r} is already in system {origin_system_id!r}."
            )

        origin_system = self._resolver.resolved_system(origin_system_id)
        if destination_system.state.map_hex_coordinate not in origin_system.state.map_hex_coordinate.neighbors:
            raise IllegalDestinationError(
                f"System {destination_system_id!r} is not a direct hex neighbor of "
                f"unit {unit_id!r}'s current system {origin_system_id!r}."
            )

        resolved_unit.state.place_in_system(destination_system_id)
