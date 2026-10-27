from dataclasses import dataclass
from typing import Self

from app.config.objs.tech import TechID
from app.state.objs import ConfigIDStateObj

@dataclass(kw_only=True)
class NekroAssimilatorTokenState(ConfigIDStateObj):
    """One of the two Valefar Assimilator tokens (config_id identifies X vs Y -
    see TechID.VALEFAR_ASSIMILATOR_X/_Y, ARCHITECTURE.md section 2)."""
    assimilated_faction_tech_id: str | None = None

    @classmethod
    def new_game(cls) -> tuple[Self, Self]:
        return (
            cls(config_id=TechID.VALEFAR_ASSIMILATOR_X.value, assimilated_faction_tech_id=None),
            cls(config_id=TechID.VALEFAR_ASSIMILATOR_Y.value, assimilated_faction_tech_id=None)
        )

    def save(self) -> dict:
        return super().save() | {
            "assimilated_faction_tech_id": self.assimilated_faction_tech_id
        }
    
    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        self.assimilated_faction_tech_id = data["assimilated_faction_tech_id"]

    def assimilate_faction_tech_id(self, faction_tech_id: str) -> None:
        self.assimilated_faction_tech_id = faction_tech_id

    def reset(self) -> None:
        self.assimilated_faction_tech_id = None

    @property
    def is_active(self) -> bool:
        return self.assimilated_faction_tech_id is not None

