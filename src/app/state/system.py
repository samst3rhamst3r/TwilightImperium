from dataclasses import dataclass
from typing import Any

from app.geometry import HexCoordinate
from app.state.base.mixins import ConfigIDInstanceMixin
from app.state.base.state_obj import StateObj

@dataclass(slots=True, kw_only=True, frozen=True)
class SystemState(StateObj, ConfigIDInstanceMixin):
    map_hex_coordinate: HexCoordinate

    def to_save_dict(self) -> dict[str, Any]:
        return {
            "map_hex_coordinate": [self.map_hex_coordinate.q, self.map_hex_coordinate.r]
        }

    def init_from_save(self, data: dict[str, Any]) -> None:
        self.map_hex_coordinate = HexCoordinate(*data["map_hex_coordinate"])
        