from dataclasses import dataclass
from typing import Any, Self
from collections.abc import Iterable

from app.config.objs.system.system import SystemConfig
from app.geometry import HexCoordinate
from app.state.base.state_obj import ConfigIDBasedStateObj

@dataclass(slots=True, kw_only=True, frozen=True)
class SystemState(ConfigIDBasedStateObj[SystemConfig]):
    map_hex_coordinate: HexCoordinate

    def to_save_dict(self) -> dict[str, Any]:
        return {
            "map_hex_coordinate": [self.map_hex_coordinate.q, self.map_hex_coordinate.r]
        }

    @classmethod
    def from_save_dict(cls, config: SystemConfig, map_hex_coordinate: Iterable[int], **kwargs) -> Self:
        return cls(config=config, map_hex_coordinate=HexCoordinate(*map_hex_coordinate), **kwargs)