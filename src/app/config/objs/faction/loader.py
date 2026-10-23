from collections.abc import Generator
from pathlib import Path

from app.config.shared.loader import load_config_obj_data
from .base import FactionConfig
from .starting_unit import FactionStartingUnitConfig

def load_faction_data(root_data_path: Path) -> Generator[FactionConfig]:
    for config in load_config_obj_data(root_data_path, "factions.yaml"):
        config["starting_tech_ids"] = tuple(config["starting_tech_ids"])
        config["starting_units"] = tuple(FactionStartingUnitConfig(**unit_config) for unit_config in config["starting_units"])
        yield FactionConfig(**config)

