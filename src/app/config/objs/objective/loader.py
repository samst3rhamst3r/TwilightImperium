from collections.abc import Generator
from pathlib import Path

from app.config.shared.loader import load_text_data_into_config_by_id
from .base import ObjectiveConfig

def load_objective_data(root_data_path: Path) -> Generator[ObjectiveConfig]:
    for config in load_text_data_into_config_by_id(root_data_path, "objectives.yaml"):
        yield ObjectiveConfig(**config)
