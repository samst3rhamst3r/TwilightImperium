from collections.abc import Generator
from pathlib import Path

from app.config.objs.ability.dispatch import PARAMETERIZED_ABILITY_INSTANCE_REGISTRY
from app.config.objs.tech import TechUpgradeReqConfig
from app.config.shared.loader import load_text_data_into_config_by_id
from .base import UnitConfig

def load_unit_data(root_data_path: Path) -> Generator[UnitConfig]:
    for config in load_text_data_into_config_by_id(root_data_path, "units.yaml", text_required=False):
        config["ability_ids"] = tuple(config.get("ability_ids", ()))
        config["upgrade_reqs"] = tuple(
            TechUpgradeReqConfig(**prereq_config) for prereq_config in config.get("upgrade_reqs", ())
        )
        config["parameterized_abilities"] = tuple(
            PARAMETERIZED_ABILITY_INSTANCE_REGISTRY[ability_config["ability_id"]](
                id=ability_config["ability_id"],
                **{key: value for key, value in ability_config.items() if key != "ability_id"},
            )
            for ability_config in config.get("parameterized_abilities", ())
        )
        yield UnitConfig(**config)
