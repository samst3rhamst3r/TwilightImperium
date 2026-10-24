from collections.abc import Generator
from pathlib import Path

from app.config.shared.loader import load_config_obj_data
from .base import ActionCardConfig

def load_action_card_data(root_data_path: Path) -> Generator[ActionCardConfig]:
    for config in load_config_obj_data(root_data_path, "action_cards.yaml"):
        config["flavor_text_options"] = tuple(config["flavor_text_options"])
        yield ActionCardConfig(**config)
