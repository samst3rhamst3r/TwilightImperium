from collections.abc import Generator
from pathlib import Path

from app.config.shared.loader import load_data, SETUP_CONFIG_DATA_PATH
from app.geometry.coordinate import HexCoordinate
from .base import MapConfig

def load_map_data(root_data_path: Path) -> Generator[MapConfig]:
    base_path = root_data_path / SETUP_CONFIG_DATA_PATH / "map"
    for path in base_path.iterdir():
        data: dict = load_data(path)
        data["tiles"] = tuple(HexCoordinate(*tile_coordinate) for tile_coordinate in data["tiles"])
        yield MapConfig(**data)
