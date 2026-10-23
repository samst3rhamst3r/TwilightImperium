from collections.abc import Generator
from pathlib import Path

from app.config.shared.loader import load_text_data_into_config_by_id
from .base import TechConfig, TechUpgradeReqConfig, StandardTechConfig, AssimilatorTechConfig
from .ids import TechID

def load_tech_data(root_data_path: Path) -> Generator[TechConfig]:
    for config in load_text_data_into_config_by_id(root_data_path, "techs.yaml"):
        config["prereqs"] = tuple(TechUpgradeReqConfig(**prereq_config) for prereq_config in config["prereqs"])
        if config["id"] in (TechID.VALEFAR_ASSIMILATOR_X, TechID.VALEFAR_ASSIMILATOR_Y):
            yield AssimilatorTechConfig(**config)
        else:
            yield StandardTechConfig(**config)
