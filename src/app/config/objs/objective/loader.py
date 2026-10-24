from collections.abc import Generator
from pathlib import Path

from app.config.shared.loader import load_config_obj_data
from .base import ObjectiveConfig

def load_objective_data(root_data_path: Path) -> Generator[ObjectiveConfig]:
    for config in load_config_obj_data(root_data_path, "objectives.yaml"):
        yield ObjectiveConfig(**config)
