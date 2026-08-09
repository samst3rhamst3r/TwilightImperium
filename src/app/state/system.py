from dataclasses import dataclass
from typing import Any

from app.geometry import HexCoordinate
from app.state.base.mixins import ConfigIDStateObj

@dataclass(slots=True, kw_only=True, frozen=True)
class SystemState(ConfigIDStateObj):
    map_hex_coordinate: HexCoordinate

    def save(self) -> dict[str, Any]:
        return super().save() | {
            "map_hex_coordinate": [self.map_hex_coordinate.q, self.map_hex_coordinate.r]
        }

    def init_from_save(self, data: dict[str, Any]) -> None:
        super().init_from_save(data)
        self.map_hex_coordinate = HexCoordinate(*data["map_hex_coordinate"])
        