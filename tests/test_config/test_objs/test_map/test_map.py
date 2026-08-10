"""Mirrors src/app/config/objs/map/map.py."""
from app.config.objs.map import MapConfig
from app.config.shared import IDConfigObj
from app.geometry.coordinate import HexCoordinate

def test_map_config_inherits_id_config_obj() -> None:
    assert issubclass(MapConfig, IDConfigObj)

def test_map_config_is_deliberately_not_kw_only() -> None:
    """Confirmed exception (see test_config_invariants._KW_ONLY_EXEMPT_DATACLASS_NAMES):
    tiles is encoded as a bare positional list of [q, r] pairs in
    data/objs/map/*.yaml to keep the hex-grid layout readable in the file."""
    assert not MapConfig.__dataclass_params__.kw_only

def test_construction_with_real_hex_coordinates() -> None:
    tiles = (HexCoordinate(0, 0), HexCoordinate(1, -1))
    map_config = MapConfig(id="mini", tiles=tiles)
    assert map_config.tiles == tiles

def test_real_map_data_has_both_shapes_present(ruleset_config) -> None:
    assert {"standard", "triangular"} <= ruleset_config.maps.keys()
