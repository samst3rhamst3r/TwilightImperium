"""Mirrors src/app/config/objs/map/map.py."""
from app.config.objs.map import MapConfig
from app.config.objs.id import IDConfigObj
from app.geometry.coordinate import HexCoordinate

def test_map_config_inherits_id_config_obj() -> None:
    assert issubclass(MapConfig, IDConfigObj)

def test_map_config_is_deliberately_not_kw_only() -> None:
    """Confirmed exception (see test_config_invariants._KW_ONLY_EXEMPT_DATACLASS_NAMES):
    tiles is encoded as a bare positional list of [q, r] pairs in
    data/setup/map/*.yaml to keep the hex-grid layout readable in the file."""
    assert not MapConfig.__dataclass_params__.kw_only

def test_construction_with_real_hex_coordinates() -> None:
    tiles = (HexCoordinate(0, 0), HexCoordinate(1, -1))
    map_config = MapConfig(id="mini", tiles=tiles)
    assert map_config.tiles == tiles

def test_from_dict_builds_hex_coordinates_from_raw_pairs() -> None:
    map_config = MapConfig.from_dict({"id": "mini", "tiles": [[0, 0], [1, -1]]})
    assert map_config.tiles == (HexCoordinate(0, 0), HexCoordinate(1, -1))

def test_real_map_data_covers_every_map_shape(map_configs) -> None:
    for shape, map_config in map_configs.items():
        assert map_config.id == shape
        assert map_config.tiles, f"{shape} map has no tiles"

def test_real_map_data_has_no_duplicate_tiles(map_configs) -> None:
    for shape, map_config in map_configs.items():
        assert len(set(map_config.tiles)) == len(map_config.tiles), f"{shape} map repeats a tile coordinate"

def test_maps_are_not_a_ruleset_config_field(ruleset_config) -> None:
    """Maps are setup-lifetime data - see ARCHITECTURE.md section 1."""
    assert not hasattr(ruleset_config, "maps")
