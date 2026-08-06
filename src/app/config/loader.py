from yaml import safe_load
from typing import Final, Any
from pathlib import Path

_BASE_CONFIG_DATA_FOLDER_PATH: Final[Path] = Path(__file__).parent.parent.parent.resolve() / "data"

def _load_data(file_name: str, base_path: Path = _BASE_CONFIG_DATA_FOLDER_PATH, include_text_data: bool = False) -> tuple[list[dict[str, Any]], ...]:

    with open(base_path / file_name) as f:
        config_data = safe_load(f)
    
    if include_text_data:
        with open(_BASE_CONFIG_DATA_FOLDER_PATH / "text" / file_name) as f:
            text_data = safe_load(f)
        return config_data, text_data
    
    return config_data,

def load_ability_data() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    return _load_data("abilities.yaml", include_text_data=True)

def load_action_card_data() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    return _load_data("action_cards.yaml", include_text_data=True)

def load_agenda_data() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    return _load_data("agendas.yaml", include_text_data=True)

def load_faction_data() -> list[dict[str, Any]]:
    return _load_data("factions.yaml")[0]

def load_map_data() -> tuple[dict[str, Any], dict[str, Any]]:
    base_path = _BASE_CONFIG_DATA_FOLDER_PATH / "map"

    triangular = _load_data("triangular.yaml", base_path=base_path)[0]
    standard = _load_data("standard.yaml", base_path=base_path)[0]

    return triangular, standard

def load_home_system_data() -> list[dict[str, list[int]]]:
    return _load_data("setup.yaml")

def load_objective_data() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    return _load_data("objectives.yaml", include_text_data=True)

def load_planet_data() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    return _load_data("planets.yaml", include_text_data=True)

def load_promissory_note_data() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    return _load_data("promissory_notes.yaml", include_text_data=True)

def load_strategy_card_data() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    return _load_data("strategy_cards.yaml", include_text_data=True)

def load_system_data() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    return _load_data("systems.yaml", include_text_data=True)

def load_tech_data() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    return _load_data("techs.yaml", include_text_data=True)

def load_unit_data() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    return _load_data("units.yaml", include_text_data=True)
