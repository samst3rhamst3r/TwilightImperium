from collections.abc import Generator
from pathlib import Path

from app.config.shared.loader import load_config_obj_data
from .base import SystemConfig

def load_system_data(root_data_path: Path) -> Generator[SystemConfig]:
    for config in load_config_obj_data(root_data_path, "systems.yaml"):
        yield SystemConfig(**config)
