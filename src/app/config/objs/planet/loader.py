from collections.abc import Generator
from pathlib import Path

from app.config.shared.loader import load_config_obj_data
from .base import PlanetConfig

def load_planet_data(root_data_path: Path) -> Generator[PlanetConfig]:
    for config in load_config_obj_data(root_data_path, "planets.yaml"):
        yield PlanetConfig(**config)
