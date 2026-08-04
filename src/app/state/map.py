from dataclasses import dataclass

@dataclass(slots=True, kw_only=True, frozen=True)
class MapState:
    map_shape_id: str