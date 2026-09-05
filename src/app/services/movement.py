from .base import BaseService

class MovementError(Exception):
    """Base for every rejection MovementService.move_unit can raise."""

class UnknownUnitError(MovementError):
    """Raised when unit_id doesn't resolve to any unit in the current game."""

class UnknownSystemError(MovementError):
    """Raised when destination_system_id doesn't resolve to any system in the current game."""

class UnitOwnershipError(MovementError):
    """Raised when requesting_player_id doesn't own the unit being moved."""

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
        try:
            resolved_unit = self._resolver.resolved_unit(unit_id)
        except KeyError:
            raise UnknownUnitError(f"No unit with id {unit_id!r} exists in this game.") from None

        try:
            destination_system = self._resolver.resolved_system(destination_system_id)
        except KeyError:
            raise UnknownSystemError(f"No system with id {destination_system_id!r} exists in this game.") from None

        if not resolved_unit.state.is_owned_by_player(requesting_player_id):
            raise UnitOwnershipError(
                f"Player {requesting_player_id!r} does not own unit {unit_id!r}."
            )

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
