from .base import BaseService

class MovementService(BaseService):

    def get_valid_systems_for_unit(self, unit_id: str):
        unit = self._resolver.resolved_unit(unit_id)
        current_loc = unit.state.location
        return unit.valid_systems_for_movement()

    def move_unit_to_system(self, unit_id: str, system_id: str):
        unit = self._resolver.resolved_unit(unit_id)
        unit.move_to_system(system_id)