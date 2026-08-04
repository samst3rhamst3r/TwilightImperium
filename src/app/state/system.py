from dataclasses import dataclass

from app.geometry import HexCoordinate
from app.state.base import ConfigIDBasedStateObj

@dataclass(slots=True, kw_only=True, frozen=True)
class SystemState(ConfigIDBasedStateObj):
    map_hex_coordinate: HexCoordinate